from datetime import datetime, timedelta
from aiohttp import ClientSession
from tortoise.models import Model
from tortoise import fields
from discord import Guild

from core import Db, cfg, Log, dc
from core.utils import random_string

from .utils import ApiError

oauth2_uri = 'https://discord.com/api/oauth2/token'
identify_uri = 'https://discord.com/api/users/@me'
guilds_uri = 'https://discord.com/api/users/@me/guilds'

"""
This module implements user authentication via discord oauth2 api. Steps:
1. From discord app authorization page user gets redirected to cfg.API_OAUTH_REDIRECT_URI?code=XXXX.
2. On the page user makes post request to do_oauth with the code.
3. _oauth_verify confirms from discord API if the code is correct and receives user_data with user access_token.
4. _oauth_fetch_user fetches user_data from the discord API (username, avatar, etc...) with the access_token.
5. do_oauth generates user api_token, replaces or creates new user in the db oauth table.
6. api_token is passed back to the user for further interactions.
Update user_data each time user_data['access_token'] is expired (@refresh_user decorator). 
"""


@Db.model
class OauthUser(Model):

    class Meta:
        __version__ = 1
    user_id = fields.BigIntField(pk=True)
    api_token = fields.CharField(max_length=256)
    user_name = fields.CharField(max_length=256)
    discriminator = fields.CharField(max_length=256)
    avatar = fields.CharField(max_length=256)
    access_token = fields.CharField(max_length=256)
    refresh_token = fields.CharField(max_length=256)
    expires_at = fields.DatetimeField()


@Db.model
class OauthUserGuild(Model):

    class Meta:
        __version__ = 1
    user_id = fields.ForeignKeyField(model_name='default_app.OauthUser', related_name='guilds', on_delete='CASCADE')
    guild_id = fields.BigIntField()


async def do_oauth(code: str) -> OauthUser:
    Log.info(f"API| Trying to auth a dc user with received oauth2 code '{code}'")
    oauth_data = await _oauth_verify(code, cfg.API_OAUTH_REDIRECT_URI, cfg.API_OAUTH_SCOPES)
    user_data = await _oauth_fetch_user(oauth_data['access_token'])

    await OauthUser.filter(user_id=user_data['id']).delete()
    oauth_user = OauthUser(
        user_id=user_data['id'],
        user_name=user_data['username'],
        discriminator=user_data['discriminator'],
        avatar=user_data['avatar'],
        api_token=random_string(8),  # TODO: make sure this is unique
        access_token=oauth_data['access_token'],
        refresh_token=oauth_data['refresh_token'],
        expires_at=datetime.now() + timedelta(seconds=oauth_data['expires_in'])
    )
    await oauth_user.save()
    return oauth_user


async def _oauth_verify(oauth_code: str, redirect_uri: str, scopes: list[str]) -> dict:
    """
    Verify oauth_code on the discord server.
    Returns oauth data response in format:
        {"access_token": str, "expires_in": int, "refresh_token": str, "scope": "identify guilds", "token_type": "Bearer" }
    """

    data = {
        'client_id': cfg.DC_CLIENT_ID,
        'client_secret': cfg.DC_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': oauth_code,
        'redirect_uri': redirect_uri,
        'scope': ' '.join(scopes)
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    async with ClientSession() as session:
        async with session.post(oauth2_uri, data=data, headers=headers) as resp:
            # Response status should be 200 if oauth_code is legit
            if resp.status != 200:
                Log.error("API| Got invalid oauth2 code {}, got {} response code from discord api.".format(oauth_code,
                                                                                                           resp.status))
                raise ApiError(400, 'Bad Request', 'Failed to authenticate.')

            oauth_data = await resp.json()
            # Check the scopes are correct
            if set(oauth_data['scope'].split(' ')) != set(scopes):
                Log.error(
                    "API| Invalid scope '{}' provided for oauth2 code '{}'".format(oauth_data['scope'], oauth_code))
                raise ApiError(400, 'Bad Request', 'Invalid oauth2 scopes provided.')

    # All good
    return oauth_data


async def _oauth_fetch_user(access_token) -> dict:
    """
    Fetch user identity using the access_token from _oauth_verify().
    Returns user data response in format:
        {
            "id": str, "username": str, "avatar": "3eec9254791b69687d29d4b2546dec7f", "discriminator": str,
            "public_flags": 0, "flags": 0, "locale": "ru", "mfa_enabled": false
        }
    """

    headers = {'Authorization': 'Bearer ' + access_token}
    async with ClientSession() as session:
        async with session.get(identify_uri, headers=headers) as resp:
            if resp.status != 200:
                Log.error(
                    "API| Error fetching user identity for access_token '{}', got {} response code from discord api".format(
                        access_token, resp.status))
                raise ApiError(500, 'Discord API error', 'Error fetching user identity')
            return await resp.json()


def refresh_user(coro):
    """ This decorator refreshes user access_token and other data on demand (if token has expired) """

    async def _update_user(oauth_user: OauthUser) -> OauthUser:
        # Get new user data
        data = {
            'client_id': cfg.DC_CLIENT_ID,
            'client_secret': cfg.DC_CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token': oauth_user.refresh_token
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        Log.info(data)

        async with ClientSession() as session:
            async with session.post('https://discord.com/api/v8/oauth2/token', data=data, headers=headers) as resp:
                if resp.status != 200:
                    Log.error(
                        'API| got invalid oauth2 refresh_token \'{}\', got {} response code from discord api'.format(
                            data['refresh_token'], resp.status
                        ))
                    raise ApiError(401, 'Bad Request', 'Failed to authenticate.')
                oauth_data = await resp.json()

        # Confirm the user_ids are matching
        if oauth_data['id'] != oauth_user.user_id:
            Log.error('API| user_id mismatching @ \'{}\' refresh_token update, expected {} got {}.'.format(
                data['refresh_token'], oauth_user.user_id, oauth_data['id']))
            raise ApiError(401, 'Bad Request', 'Failed to authenticate.')

        # Push to database

        new_oauth_user = OauthUser(
            user_id=oauth_data['id'],
            user_name=oauth_data['username'],
            discriminator=oauth_data['discriminator'],
            avatar=oauth_data['avatar'],
            api_token=oauth_user.api_token,
            access_token=oauth_data['access_token'],
            refresh_token=oauth_data['refresh_token'],
            expires_at=datetime.now() + timedelta(seconds=oauth_data['expires_in'])
        )
        await new_oauth_user.save()
        return new_oauth_user

    async def wrapper(oauth_user: OauthUser, *args, **kwargs):
        if OauthUser.expires_at < datetime.now():
            oauth_user = await _update_user(oauth_user)
        return await coro(oauth_user, *args, **kwargs)

    return wrapper


@refresh_user
async def fetch_user_guilds(oauth_user: OauthUser) -> list[Guild]:
    """
    Fetch user's guild list from discord api. API response format:
        [{"id": str, "name": str, "icon": "8342729096ea3675442027381ff50dfe", "owner": true, "permissions": "36953089", "features": ["COMMUNITY", "NEWS"]}]
    Updates oauth_user_guilds for the lazy method.
    Returns list with discord.Guild objects.
    """

    headers = {'Authorization': 'Bearer ' + oauth_user['access_token']}
    async with ClientSession() as session:
        async with session.get(guilds_uri, headers=headers) as resp:
            if resp.status != 200:
                Log.error(
                    f"API| Error fetching guilds list for access_token '{oauth_user['access_token']}', resp.code {resp.status}"
                )
                raise ApiError(500, 'Discord API error', 'Error fetching guild list.')
            guilds_data = await resp.json()

    await oauth_user.guilds.all().delete()
    await OauthUserGuild.bulk_create(
        [OauthUserGuild(user_id=oauth_user.user_id, guild_id=int(g['id'])) for g in guilds_data]
    )

    return [g for g in dc.guilds if g.id in [int(i['id']) for i in guilds_data]]


async def get_user_guilds(oauth_user: OauthUser) -> list[Guild]:
    """ Get user guilds from db (lazy method) """

    guild_ids = [i.guild_id for i in await oauth_user.guilds.all()]
    return [g for g in dc.guilds if g.id in guild_ids]


async def get_user(api_token: str) -> OauthUser:
    """ Return oauth_user data for an api_token or raise an exception """
    if (oauth_user := await OauthUser.get_or_none(api_token=api_token)) is None:
        raise ApiError(400, 'API error', 'Bad api_token.')
    return oauth_user


async def delete_user(oauth_user: OauthUser) -> None:
    await oauth_user.delete()

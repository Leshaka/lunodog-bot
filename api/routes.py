from aiohttp.web import Request

from . import ApiRoute, ApiError, api_success, oauth


@ApiRoute('/test', method='GET', auth=False)
async def test(request: Request):
    return api_success({'message': 'That is an API answer!'})


# Client should get redirected to this route from discord oauth url like:
# https://discord.com/api/oauth2/authorize?
#   client_id={DC_CLIENT_ID}&redirect_uri={API_OAUTH_REDIRECT_URI}&response_type=code&scope={' '.join(API_OAUTH_SCOPES)}
# But in this case client gets redirected to the vuejs oauth page, that passes the url query to this route as post
@ApiRoute('/oauth', method='POST', auth=False)
async def do_oauth(request: Request, code=None):
    if code is None:
        raise ApiError(code=400, title='Bad Request', message='Oauth2 code is missing in the request.')

    oauth_user = await oauth.do_oauth(code)
    response = api_success()
    response.set_cookie('api_token', oauth_user.api_token, samesite=None, secure=True)
    return response


@ApiRoute('/test_authed', method='GET', auth=True)
async def test_authed(request: Request, oauth_user: oauth.OauthUser):
    return api_success({'success': f'Authed as {oauth_user.user_name}'})


@ApiRoute('/get_user', method='GET', auth=True)
async def get_user(request: Request, oauth_user: oauth.OauthUser):
    return api_success({
        'id': oauth_user.user_id,
        'name': oauth_user.user_name,
        'discriminator': oauth_user.discriminator,
        'avatar': oauth_user.avatar,
        'guilds': [
            {'id': g.id, 'name': g.name, 'icon': g.icon}
            for g in await oauth.get_user_guilds(oauth_user)
        ]
    })

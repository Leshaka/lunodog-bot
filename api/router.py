from aiohttp import web
import traceback
import json

from core import Log
from modules.bot import Bot
from . import ApiServer, oauth, ApiError


class ApiRoute:
    """
    This class is a decorator for API route functions. It does:
        Register routes with '/api' prefix.
        Prevent calling the function if connection to discord is not ready.
        Provide oauth_user if auth=True is passed.
        Provide post json data as kwargs.
        Handle regular (ApiError) exceptions.
        Handle unexpected exceptions.
    """

    def __init__(self, path, method='GET', auth=False):
        self.path = path
        self.method = method
        self.auth = auth

    def __call__(self, coro):
        async def decorator(request):
            return await self.wrapper(request, coro)

        Log.info(f"API| registering route /api{self.path}")
        ApiServer.app.router.add_route(self.method, '/api' + self.path, decorator)
        return decorator

    # Main function
    async def wrapper(self, request: web.Request, coro):
        # Check if the bot is ready to process api requests.
        if not Bot.bot_ready:
            return ApiError(code=503, title="Bot is under connection.",
                            message="Please try again later...").web_response()

        # Prepare kwargs and run the function
        try:
            kwargs = await self.get_post_data(request) if self.method == 'POST' else dict(request.query)

            if self.auth:
                kwargs['oauth_user'] = await self.get_oauth_user(request)

            Log.info(f"Running {coro.__name__}...")
            return await coro(request, **kwargs)

        # Catch regular exceptions
        except ApiError as e:
            return e.web_response()

        # Catch unexpected exceptions
        except (Exception, BaseException) as e:
            Log.error("\n".join([
                "API request failed with an unexpected exception!",
                f"URL: {request.rel_url}",
                f"Error: {e}",
                f"Traceback: {traceback.format_exc()}"
            ]))
            return ApiError(code=500, title="Internal Server Error", message="Unknown API error.").web_response()

    @staticmethod
    async def get_post_data(request):
        try:
            data = await request.json()
        except json.decoder.JSONDecodeError:
            return ApiError(code=400, title="API error.", message="Bad post data.").web_response()
        else:
            return data

    @staticmethod
    async def get_oauth_user(request):
        if (api_token := request.cookies.get('api_token')) is None:
            raise ApiError(401, 'Not authorized', 'api_token is missing.')
        return await oauth.get_user(api_token)

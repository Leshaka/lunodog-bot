from aiohttp.web import Response
import json


class ApiError(Exception):

    def __init__(self, code=500, title="Internal Server Error", message="There was an error processing the request."):
        self.code = code
        self.title = title
        self.message = message

    def web_response(self):
        return Response(
            status=self.code,
            content_type='application/json',
            body=json.dumps({'error': {'status': self.title, 'message': self.message}})
        )


def api_success(data=None):
    """ Convert data to json and send good response """
    return Response(
        status=200,
        content_type='application/json',
        body=json.dumps({'status': 'ok'} if data is None else data)
    )

from apistar import http, exceptions
from users.models import User
from project.settings import NO_AUTH_ENDPOINTS, ORIGIN


class Cors():
    def on_response(self, response: http.Response):
        response.headers['Access-Control-Allow-Origin'] = ORIGIN


class MustBeAuthenticated():
    def on_request(self, path: http.Path, user: User=None) -> None:
        white_list = NO_AUTH_ENDPOINTS
        white_list = list(map(lambda x: x.replace('/', ''), white_list))
        path = path.replace('/', '')
        if user is None and path not in white_list:
            raise exceptions.HTTPException('Unauthorized', 401)

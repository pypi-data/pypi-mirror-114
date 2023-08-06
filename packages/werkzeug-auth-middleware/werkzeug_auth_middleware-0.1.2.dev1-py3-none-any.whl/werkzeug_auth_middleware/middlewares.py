from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException
import requests
import json
from os import getenv


class UserProfileInjectorMiddleware:
    '''
    Simple WSGI Middleware to enforce authentication in microservices architecture
    '''

    def __init__(self, app, exempted_endpoints=None):
        exempted_endpoints = exempted_endpoints or []

        self.app = app
        self.exempted_endpoints = [endpoint for endpoint in exempted_endpoints]
        assert getenv("USER_PROFILE_URL") != None

    def get_access_token(self):
        access_token = self.request.headers.get("Authorization")
        if not access_token:
            raise HTTPException(response=Response(json.dumps({"message": "User not authenticated"}), mimetype='application/json', status=401))
        return True

    def get_user_profile(self):
        response = requests.get(
            getenv("USER_PROFILE_URL"), headers=self.request.headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(response=Response(json.dumps({"message": "Cannot get user profile"}), mimetype='application/json', status=401))

    def __call__(self, environ, start_response):
        self.request = Request(environ)

        if self.request.url in self.exempted_endpoints:
            return self.app(environ, start_response)

        try:
            user_profile = self.get_access_token() and self.get_user_profile()
            # environ are not passed to subsequent function, instead the original request data is passed
            # save generated request in the 
            environ['User-Profile'] = user_profile
            return self.app(environ, start_response)
        except HTTPException as e:
            return e.response(environ, start_response)

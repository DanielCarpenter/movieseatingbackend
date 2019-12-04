from modules.access import access_api
from .controllers import ApiLogin, TokenRefresh

access_api.add_resource(ApiLogin, '/access')
access_api.add_resource(TokenRefresh, '/access/refresh')

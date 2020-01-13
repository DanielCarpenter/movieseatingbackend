from modules.accounts import account_api
from .controllers import ApiRegister, ApiLogin, TokenRefresh

account_api.add_resource(ApiRegister, '/users')
account_api.add_resource(ApiLogin, '/login')
account_api.add_resource(TokenRefresh, '/refresh')
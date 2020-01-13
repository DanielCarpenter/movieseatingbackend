from modules.accounts import account_api
from .controllers import ApiRegister, ApiLogin, TokenRefresh
from .showing_controller import ShowingList, OneShowing, OneSeat

account_api.add_resource(ApiRegister, '/register')
account_api.add_resource(ApiLogin, '/login')
account_api.add_resource(TokenRefresh, '/refresh')
account_api.add_resource(ShowingList, '/showing/all')
account_api.add_resource(OneShowing, '/showing')
account_api.add_resource(OneSeat, '/reserve')


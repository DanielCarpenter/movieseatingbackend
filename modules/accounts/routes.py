from modules.accounts import register_api
from .controllers import ApiRegister

register_api.add_resource(ApiRegister, '/reg')
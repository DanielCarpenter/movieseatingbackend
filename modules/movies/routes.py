from . import movies_api
from .controllers import OneMovie, MovieList

movies_api.add_resource(OneMovie, '/movie')
movies_api.add_resource(MovieList, '/movie/all')

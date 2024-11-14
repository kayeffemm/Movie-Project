from classes.movie_app import MovieApp
from classes.storage_json import StorageJson

storage = StorageJson("data/movie_database.json")
movie_app = MovieApp(storage)

movie_app.run()
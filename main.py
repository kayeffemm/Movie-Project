from classes.movie_app import MovieApp
from classes.storage_json import StorageJson
from classes.storage_csv import StorageCSV


HTML_TEMPLATE_PATH = 'static/index_template.html'
HTML_OUTPUT_PATH = 'static/index.html'


def main():
    """
    Instantiate IStorage object, MovieApp object and call the run method from MovieApp object.
    """
    storage_json = StorageJson('data/movie_database.json')
    movie_app_json = MovieApp(storage_json, HTML_TEMPLATE_PATH, HTML_OUTPUT_PATH)

    storage_csv = StorageCSV('data/movie_database.CSV')
    movie_app_csv = MovieApp(storage_csv, HTML_TEMPLATE_PATH, HTML_OUTPUT_PATH)

    # Choose one of them. Command line argument to start coming soon.
    #movie_app_json.run()
    movie_app_csv.run()


if __name__ == "__main__":
    main()
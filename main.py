import sys
from movie_app.movie_app import MovieApp
from storage.storage_json import StorageJson
from storage.storage_csv import StorageCSV


HTML_TEMPLATE_PATH = 'static/index_template.html'
HTML_OUTPUT_PATH = 'static/index.html'


def main():
    """
    Instantiate IStorage object, MovieApp object and call the run method from MovieApp object.
    """
    if check_sys_input():
        filetype, username = check_sys_input()
        if filetype == 'csv':
            print(f"\nWelcome {username}, you're using your csv database.")
            storage = StorageCSV(f'data/{username}_movie_database.csv')
            movie_app = MovieApp(storage, HTML_TEMPLATE_PATH, HTML_OUTPUT_PATH)
            movie_app.run()
        elif filetype == 'json':
            print(f"\nWelcome {username}, you're using your json database.")
            storage = StorageJson(f'data/{username}_movie_database.json')
            movie_app = MovieApp(storage, HTML_TEMPLATE_PATH, HTML_OUTPUT_PATH)
            movie_app.run()
    else:
        print("""
        No parameters given or invalid.
        Remember: Parameters have to end with .csv or .json
        Starting program with default database, feel free to quit.
        """)
        storage = StorageJson('data/movie_database.json')
        movie_app = MovieApp(storage,HTML_TEMPLATE_PATH, HTML_OUTPUT_PATH)
        movie_app.run()


def check_sys_input() -> None|tuple:
    if len(sys.argv) > 1:
        user_data = sys.argv[1].lower()
        if user_data.endswith('.csv'):
            filetype = 'csv'
            username = user_data[0:-4]
        elif user_data.endswith('.json'):
            filetype = 'json'
            username = user_data[0:-5]
        else:
            return None
        return filetype, username
    return None


if __name__ == "__main__":
    main()
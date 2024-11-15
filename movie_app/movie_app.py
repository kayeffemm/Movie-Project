import statistics, random, requests, os
from storage.istorage import IStorage
from dotenv import load_dotenv


class MovieApp:
    def __init__(self, storage, html_template_path: str, html_output_path: str) -> None:
        if not isinstance(storage, IStorage):
            raise TypeError(f"Expected storage to be instance of IStorage, got {type(storage).__name__} instead.")
        self._storage = storage
        self._html_template_path = html_template_path
        self._html_output_path = html_output_path

        load_dotenv()
        self._api_key = os.getenv('API_KEY')

    def list_movies(self):
        """
        Gets data from self._storage.get_movies_data() and prints out
        all the movies currently existing in movie_database.json
        """
        movies = self._storage.get_movies_data()
        print(f"{len(movies)} movies in total")
        for movie in movies:
            movie_name = movie["title"]
            movie_rating = movie["rating"]
            movie_year = movie["year"]
            print(f"{movie_name} ({movie_year}): {movie_rating}")

    def add_movies(self):
        """
        Asks user for multiple inputs, checks if they are valid.
        If not user is prompted to type again until its valid.
        Then the inputs get parsed to self._storage.write_movie_data()
        """
        while True:
            user_input_movie_title = input("Enter a movie Title: ").strip()
            if not user_input_movie_title:
                print("Movie name can't be empty")
            if user_input_movie_title:
                res = self._get_movie_by_name_from_omdb_api(user_input_movie_title)
                if res is not None:
                    movie_title, movie_year, movie_rating, movie_poster_url = self._extract_info_from_movie_dict(res)
                    break
                else:
                    print("Movie not found in OMDB, try again.")
        if self._movie_already_exists(movie_title):
            print(f"Movie {movie_title} already exists in your database.")
        else:
            self._storage.write_movies_data(movie_title, movie_year, movie_rating, movie_poster_url)
            print(f"Movie {movie_title} successfully added")

    def _movie_already_exists(self, title: str) -> bool:
        """Check current storage if movie is already present, returns bool"""
        movie_exists = False
        for item in self._storage.get_movies_data():
            if title == item['title']:
                movie_exists = True
        return movie_exists

    @staticmethod
    def _extract_info_from_movie_dict(res: dict) -> tuple[str, int, float, str]:
        """Grabs only needed information from dictionary, saves into variable and returns a tuple"""
        title = res["Title"]
        year = int(res["Year"][0:4])
        try: # If movie got no rating return default rating -> 0.0
            rating = float(res['imdbRating'])
        except ValueError:
            rating = 0.0
        poster = res['Poster']
        return title, year, rating, poster

    def _get_movie_by_name_from_omdb_api(self, name: str) -> dict|None:
        """
        Parse movie name to OMDB API, fetch a JSON and convert to dict.
        """
        try:
            res = requests.get(f'http://www.omdbapi.com/?i=tt3896198&apikey={self._api_key}&t={name}')
            res = res.json()
            if self._validate_request(res):
                return res
            else:
                return None
        except Exception as e:
            print("Error:", e)
            return None

    @staticmethod
    def _validate_request(res: dict) -> bool:
        """Check if returned dict from request has valid data"""
        return 'Title' in res.keys()

    def delete_movie(self):
        """
        Asks user for movie to delete.
        Then parses the string to self._storage.delete_movie_data()
        If movie doesn't exist it lets the user know.
        """
        movies = self._storage.get_movies_data()
        movie_titles = [movie["title"] for movie in movies]
        user_input_movie_name = input("Enter name of movie you want to delete: ")

        if user_input_movie_name in movie_titles:
            self._storage.delete_movie_data(user_input_movie_name)
            print(f"Movie {user_input_movie_name} successfully deleted!")
        else:
            print(f"Movie {user_input_movie_name} doesn't exist!")

    def update_movie(self):
        """
        Asks user for movie name to update.
        If movie exist in database user is prompted to enter a new rating.
        If movie doesn't exist prints an error message.
        """
        movies = self._storage.get_movies_data()
        movie_titles = [movie["title"] for movie in movies]
        user_input_movie_name = input("Enter name of movie you want to update: ")

        if user_input_movie_name in movie_titles:
            while True:
                try:
                    user_input_new_rating = float(input("Enter new movie rating: "))
                    self._storage.update_movie_data(user_input_movie_name, user_input_new_rating)
                    print("rating successfully changed!")
                    break
                except ValueError:
                    print("Please enter a valid rating")
        else:
            print(f"Movie {user_input_movie_name} doesn't exist!")

    def movie_stats(self):
        """
        Calls list_movies function to get all data and prints the average, median rating.
        Also identifies the worst and best movies and saves them to a list.
        Then parses both lists to print_list_of_tuple function to get a printable string.
        """
        movies = self._storage.get_movies_data()
        rating_list = [float(movie["rating"]) for movie in movies]

        average_rating = sum(rating_list) / len(rating_list)
        median_rating = statistics.median(rating_list)

        best_rating = max(rating_list)
        worst_rating = min(rating_list)

        best_movies = [(movie["title"], movie["rating"]) for movie in movies if float(movie["rating"]) == best_rating]
        worst_movies = [(movie["title"], movie["rating"]) for movie in movies if float(movie["rating"]) == worst_rating]

        print(f"Average rating: {round(average_rating, 1)}")
        print(f"Median rating: {round(median_rating, 1)}")
        print(f"Best movie(s): {self.get_printable_string_from_tuple(best_movies)}")
        print(f"Worst movie(s): {self.get_printable_string_from_tuple(worst_movies)}")

    def random_movie(self):
        """
        uses the random module to get a pseudo-random entry from the movies list and prints it.
        """
        movies = self._storage.get_movies_data()
        random_movie_dictionary = random.choice(movies)
        title = random_movie_dictionary["title"]
        rating = random_movie_dictionary["rating"]
        print(f"You could watch this movie: {title}, it\'s rated {rating}")

    def search_movie(self):
        """
        Gets movies data from self._storage.get_movies_data() and asks user to enter part
        of a movie name.
        Creates a list of tuples to save all movies and their index in a list of tuples.
        Then iterates over the created list and checks if user search term is part of any movie name,
        if that's the case it saves this movies index in a different list.
        At the end it checks if there were any matching movies found, if not user gets an error message.
        If any movie(s) were found it iterates over the movies list of dictionaries and prints out every movie with
        a matching index from the matching_movies_by_index list.
        """
        movies = self._storage.get_movies_data()
        user_search_term = input("Enter part of movie name: ")
        all_movie_titles_with_index = [(i, movie["title"]) for i, movie in enumerate(movies)]

        matching_movie_by_index = []
        for index, movie_title in enumerate(all_movie_titles_with_index):
            if user_search_term.lower() in str(movie_title[1]).lower():
                matching_movie_by_index.append(index)

        if len(matching_movie_by_index) == 0:
            print("Movie name not found!")
        else:
            for i, movie in enumerate(movies):
                if i in matching_movie_by_index:
                    print(f"{movie["title"]} ({movie["year"]}): {movie["rating"]}")

    def movies_sorted_by_rating(self):
        """
        uses sorted() function to create a list of movies sorted by their rating.
        Next it iterates over said list and prints out all movies with their info.
        """
        movies = self._storage.get_movies_data()
        movies_sorted_by_rating_list = sorted(movies, key=lambda x: x["rating"], reverse=True)
        for movie in movies_sorted_by_rating_list:
            print(f"{movie["title"]} ({movie["year"]}): {movie["rating"]}")

    def movies_sorted_by_year(self):
        """
        Asks user for sorting order.
        Then uses sorted() function to create a list of movies sorted by their release year.
        Next it iterates over said list and prints out all movies with their info.
        """
        movies = self._storage.get_movies_data()
        descending_order = False
        while True:
            user_choice = input("Do you want the latest movies first? (Y/N)\n")
            if user_choice.lower() == "y":
                descending_order = True
                break
            elif user_choice.lower() == "n":
                break
            else:
                print("Please enter 'Y' or 'N'")

        movies_sorted_by_year_list = sorted(movies, key=lambda x: x["year"], reverse=descending_order)
        for movie in movies_sorted_by_year_list:
            print(f"{movie["title"]} ({movie["year"]}): {movie["rating"]}")

    def filter_movies(self):
        """
        Asks user for filter criteria, validates input with get_float_input() and get_int_input()
        and creates a new list with filter applied.
        If there are movies matching the filter prints them out, if not it prints an error message.
        """
        movies = self._storage.get_movies_data()
        minimum_rating = self.get_float_input("Enter minimum rating, leave blank for no filter: ")
        start_year = self.get_int_input("Enter start year, leave blank for no filter: ")
        end_year = self.get_float_input("Enter end year, leave blank for no filter: ")

        filtered_movies = []
        for movie in movies:
            if minimum_rating is not None and movie["rating"] < minimum_rating:
                continue
            if start_year is not None and movie["year"] < start_year:
                continue
            if end_year is not None and movie["year"] > end_year:
                continue
            filtered_movies.append(movie)

        if filtered_movies:
            print("Filtered movies:")
            for movie in filtered_movies:
                print(f"{movie["title"]} ({movie["year"]}): {movie["rating"]}")
        else:
            print("\nThere are no movies with your filters applied.")

    def generate_website(self):
        """"""
        from movie_app.website_generator import WebsiteGenerator
        movies = self._storage.get_movies_data()
        generator = WebsiteGenerator(movies, self._html_template_path, self._html_output_path)
        generator.generate_website()
        print("Website successfully created!")

    @staticmethod
    def get_printable_string_from_tuple(a_list: list[tuple]) -> str:
        """
        Helper function to convert list of tuples into a string and returns it.
        :return: fstring
        """
        if len(a_list) > 1:
            string_to_print = ""
            for item in a_list:
                string_to_print += f"({item[0]}, {item[1]}) "
            return string_to_print
        else:
            return f"{a_list[0][0]}, {a_list[0][1]}"

    @staticmethod
    def get_float_input(prompt: str):
        """
        validates user input if its empty or able to convert into float
        :return: None or Converted Input
        """
        while True:
            user_input = input(prompt)
            if user_input == "":
                return None
            try:
                return float(user_input)
            except ValueError:
                print("Invalid, please enter a number!")

    @staticmethod
    def get_int_input(prompt: str):
        """
        validates user input if its empty or able to convert into float
        :return: None or Converted Input
        """
        while True:
            user_input = input(prompt)
            if user_input == "":
                return None
            try:
                return float(user_input)
            except ValueError:
                print("Invalid, please enter a number!")

    def run(self) -> None:
        """Instantiates MovieMenu to run the menu"""
        from movie_app.movie_menu import MovieMenu
        movie_menu = MovieMenu()
        movie_menu.run(self)


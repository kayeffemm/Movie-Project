class MovieMenu:
    def __str__(self) -> str:
        """
        This method will manually return the menu as a string.
        Needs to be updated according to changes in MovieApp class.
        """
        return """
        1. Add movie
        2. Delete movie
        3. Filter movies
        4. Movie stats
        5. Get a random movie
        6. Search movie
        7. Movies sorted by rating
        8. Movies sorted by year
        9. List all movies
        10. Update movie
        11. Generate Website
        Q. Quit
        """

    def run(self, movie_app) -> None:
        """
        This method will handle user input and execute the corresponding method from MovieApp.
        """
        while True:
            print(self)
            user_input = input("Choose an action: ").strip().lower()

            match user_input:
                case 'q' | 'quit':
                    print("Exiting the menu.")
                    break
                case '1':
                    movie_app.add_movies()
                case '2':
                    movie_app.delete_movie()
                case '3':
                    movie_app.filter_movies()
                case '4':
                    movie_app.movie_stats()
                case '5':
                    movie_app.random_movie()
                case '6':
                    movie_app.search_movie()
                case '7':
                    movie_app.movies_sorted_by_rating()
                case '8':
                    movie_app.movies_sorted_by_year()
                case '9':
                    movie_app.list_movies()
                case '10':
                    movie_app.update_movie()
                case '11':
                    movie_app.generate_website()
                case _:
                    print("Invalid input, please try again.")

            #buffer
            input("\nPress Enter to continue to the menu.")
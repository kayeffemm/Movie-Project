
class WebsiteGenerator:
    def __init__(self, movies: list[dict], html_template_path: str, html_output_path: str) -> None:
        """initialize Placeholder constant and movie variable"""
        self.placeholder = "__TEMPLATE_MOVIE_GRID__"
        self._movies = movies
        self._html_template_path = html_template_path
        self._html_output_path = html_output_path

    def generate_website(self) -> None:
        """
        Main method for the class:
        - Reads the HTML template.
        - Gets data from self._movies and generates HTML content.
        - Writes the HTML content to a specified output file.
        """
        html_template = self.__html_template_to_string()
        movie_content = self.__generate_html_string()
        new_html_string = self.__add_data_to_template(html_template, movie_content)
        self.__write_html_file(self._html_output_path, new_html_string)

    def __html_template_to_string(self) -> str:
        """Opens HTML Template and returns it as a string"""
        with open(self._html_template_path, 'r') as template:
            return template.read()

    def __add_data_to_template(self, template: str, content: str) -> str:
        """Replaces Placeholder in template with new content and returns it"""
        return template.replace(self.placeholder, content)

    def __generate_html_string(self) -> str:
        """Generates an HTML string based on self._movies"""
        return "".join(self.__serialize_movie(movie) for movie in self._movies)

    @staticmethod
    def __serialize_movie(movie: dict) -> str:
        """Serialize a single movie into an HTML string representation."""
        movie_title = movie.get('title')
        movie_year = movie.get('year')
        movie_poster = movie.get('poster_url')

        html_string = '\t\t<li>\n'
        html_string += '\t\t\t<div class="movie">\n'
        html_string += f'\t\t\t\t<img class="movie-poster" src="{movie_poster}">\n'
        html_string += f'\t\t\t\t<div class="movie-title">{movie_title}</div>\n'
        html_string += f'\t\t\t\t<div class="movie-year">{movie_year}</div>\n'
        html_string += '\t\t\t</div>\n'
        html_string += '\t\t</li>\n'

        return html_string

    @staticmethod
    def __write_html_file(output_path: str, content: str) -> None:
        """Creates / overwrites html file at specified location with new content"""
        with open(output_path, "w") as new_file:
            new_file.write(content)
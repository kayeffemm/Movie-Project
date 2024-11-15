import json
import os.path
from storage.istorage import IStorage


class StorageJson(IStorage):
    """Handle data when working with a JSON"""
    def __init__(self, file_path: str):
        """Initializes self._file_path"""
        if not isinstance(file_path, str):
            raise TypeError(f"Expected string for file_path, got {type(file_path).__name__} instead.")
        if not file_path.strip():
            raise ValueError(f"Empty string is invalid")

        self._filepath = file_path

    def get_movies_data(self) -> list[dict]:
        """
        Calls validate_data() to verify file integrity.
        If everything is fine the function loads the information from
        the JSON file and returns the data as a list of dictionaries
        :return: list[dict]
        """
        if not self.validate_data():
            print("Loading default data due to prior data issues.")

        with open(self._filepath, "r") as file_reader:
            data = json.load(file_reader)
        return data

    def write_movies_data(self, title: str, year: int, rating: float, poster_url: str) -> None:
        """
        Adds a movie to the database.
        Loads the information from the JSON file, add the movie,
        and saves it. The function doesn't need to validate the input.
        """
        movies = self.get_movies_data()
        movies.append({
            "title": title,
            "year": year,
            "rating": rating,
            "poster_url": poster_url
        })

        with open(self._filepath, "w") as file_writer:
            json.dump(movies, file_writer, indent=4)

    def delete_movie_data(self, title: str) -> None:
        """
        Deletes a movie from the database.
        Loads the information from get_movies_data(), deletes the movie,
        and saves it. The function doesn't need to validate the input.
        """
        movies = self.get_movies_data()
        del movies[next(i for i, movie in enumerate(movies) if movie["title"] == title)]

        with open(self._filepath, "w") as file_writer:
            json.dump(movies, file_writer, indent=4)

    def update_movie_data(self, title: str, note: str) -> None:
        """
        Updates a movie from the database.
        Loads the information from get_movies_data(), updates the movie,
        and saves it. The function doesn't need to validate the input.
        """
        movies = self.get_movies_data()
        index_of_dictionary_to_update = next(i for i, movie in enumerate(movies) if movie["title"] == title)
        movies[index_of_dictionary_to_update]["note"] = note

        with open(self._filepath, "w") as file_writer:
            json.dump(movies, file_writer, indent=4)

    def secure_existence(self) -> bool:
        """
        Checks if the file exists and returns True, if file does not exist
        calls write_default_data and returns True, so validate_data can continue with validating
        """
        if not os.path.isfile(self._filepath):
            print("File does not exist, creating default Data")
            self.write_default_data()
        return True

    def validate_data(self) -> bool:
        """
        Calls validate_existence() to check if there is any data,
        if there is data to work with it reads the data and checks
        if data is valid. In case data is invalid it calls write_default_data()
        :returns: boolean
        :todo: separate creation and validity
        """
        data_exists = self.secure_existence()
        if data_exists:
            try:
                with open(self._filepath, "r") as json_file:
                    data = json.load(json_file)
                    if len(data) >= 1 and data != "[]":
                        return True
                    else:
                        self.write_default_data()
            except json.decoder.JSONDecodeError:
                print("File data missing or corrupted, creating default Data")
                self.write_default_data()
                return False

    def write_default_data(self) -> None:
        """
        gets called if data is not existent or invalid and
        writes some default data
        """
        default_data = [{
            "title": "Fight Club",
            "year": 1999,
            "rating": 8.8,
            "poster_url": "https://m.media-amazon.com/images/M/MV5BOTgyOGQ1NDItNGU3Ny00MjU3LTg2YWEtNmEyYjBiMjI1Y2M5XkEyXkFqcGc@._V1_SX300.jpg"
        }]
        with open(self._filepath, "w") as file_writer:
            json.dump(default_data, file_writer, indent=4)

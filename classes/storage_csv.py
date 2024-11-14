import csv
import os.path
from classes.istorage import IStorage

class StorageCSV(IStorage):
    """Handle data when working with a CSV"""
    def __init__(self, file_path: str):
        """Initializes self._file_path"""
        if not isinstance(file_path, str):
            raise TypeError(f"Expected string for file_path, got {type(file_path).__name__} instead.")
        if not file_path.strip():
            raise ValueError("Empty string is invalid")

        self._filepath = file_path

    def get_movies_data(self) -> list[dict]:
        """
        Calls validate_data() to verify file integrity.
        If everything is fine, the function loads the information from
        the CSV file and returns the data as a list of dictionaries.
        :return: list[dict]
        """
        if not self.validate_data():
            print("Loading default data due to prior data issues.")

        movies = []
        with open(self._filepath, "r", newline='', encoding='utf-8') as file_reader:
            csv_reader = csv.DictReader(file_reader)
            for row in csv_reader:
                row['year'] = int(row['year'])
                row['rating'] = float(row['rating'])
                movies.append(row)
        return movies

    def write_movies_data(self, title: str, year: int, rating: float, *poster) -> None:
        """
        Adds a movie to the database.
        Loads the information from the CSV file, adds the movie,
        and saves it.
        """
        movies = self.get_movies_data()
        movies.append({
            "title": title,
            "year": year,
            "rating": rating
        })

        with open(self._filepath, "w", newline='', encoding='utf-8') as file_writer:
            csv_writer = csv.DictWriter(file_writer, fieldnames=["title", "year", "rating"])
            csv_writer.writeheader()
            csv_writer.writerows(movies)

    def delete_movie_data(self, title: str) -> None:
        """
        Deletes a movie from the database.
        Loads the information from get_movies_data(), deletes the movie,
        and saves it.
        """
        movies = self.get_movies_data()
        movies = [movie for movie in movies if movie["title"] != title]

        with open(self._filepath, "w", newline='', encoding='utf-8') as file_writer:
            csv_writer = csv.DictWriter(file_writer, fieldnames=["title", "year", "rating"])
            csv_writer.writeheader()
            csv_writer.writerows(movies)

    def update_movie_data(self, title: str, rating: float) -> None:
        """
        Updates a movie in the database.
        Loads the information from get_movies_data(), updates the movie,
        and saves it.
        """
        movies = self.get_movies_data()
        for movie in movies:
            if movie["title"] == title:
                movie["rating"] = rating

        with open(self._filepath, "w", newline='', encoding='utf-8') as file_writer:
            csv_writer = csv.DictWriter(file_writer, fieldnames=["title", "year", "rating"])
            csv_writer.writeheader()
            csv_writer.writerows(movies)

    def secure_existence(self) -> bool:
        """
        Checks if the file exists and returns True. If the file does not exist,
        it calls write_default_data and returns True.
        """
        if not os.path.isfile(self._filepath):
            print("File does not exist, creating default Data")
            self.write_default_data()
        return True

    def validate_data(self) -> bool:
        """
        Calls secure_existence() to check if there is any data.
        If there is data to work with, it reads the data and checks
        if the data is valid. In case the data is invalid, it calls write_default_data()
        :returns: boolean
        """
        data_exists = self.secure_existence()
        if data_exists:
            try:
                with open(self._filepath, "r", newline='', encoding='utf-8') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    rows = list(csv_reader)
                    if len(rows) > 1:
                        return True
            except csv.Error:
                print("File data missing or corrupted, creating default Data")
                self.write_default_data()
                return False

    def write_default_data(self) -> None:
        """
        Gets called if data is nonexistent or invalid and
        writes some default data.
        """
        default_data = [{
            "title": "Fight Club",
            "year": 1999,
            "rating": 8.8
        }]
        with open(self._filepath, "w", newline='', encoding='utf-8') as file_writer:
            csv_writer = csv.DictWriter(file_writer, fieldnames=["title", "year", "rating"])
            csv_writer.writeheader()
            csv_writer.writerows(default_data)

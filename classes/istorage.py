from abc import ABC, abstractmethod


class IStorage(ABC):
    """
    Abstract interface class which includes function definitions to implement in its subclasses
    """
    @abstractmethod
    def get_movies_data(self):
        """List all movies from database"""
        pass

    @abstractmethod
    def write_movies_data(self, title: str, year: int, rating: float, poster) -> None:
        """Add a movie to the database"""
        pass

    @abstractmethod
    def delete_movie_data(self, title: str) -> None:
        """Delete a movie from database"""
        pass

    @abstractmethod
    def update_movie_data(self, title: str, rating: float) -> None:
        """Update movie data in database"""
        pass

    @abstractmethod
    def validate_existence(self) -> bool:
        """Checks if requested file does exist, returns bool"""
        pass

    @abstractmethod
    def validate_data(self) -> bool:
        """Checks if requested data is valid, returns True if valid or calls write_default_data if data invalid"""
        pass

    @abstractmethod
    def write_default_data(self) -> None:
        """Writes default data"""
        pass

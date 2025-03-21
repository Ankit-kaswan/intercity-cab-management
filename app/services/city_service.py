from sqlalchemy.orm import Session
from app.repositories.city_repository import CityRepository
from app.schemas import CityCreate


class CityService:

    @staticmethod
    def register_city(db: Session, city_data: CityCreate):
        """Registers a new city."""
        return CityRepository.create_city(db, city_data.dict())

    @staticmethod
    def get_all_cities(db: Session):
        """Retrieves all registered cities."""
        return CityRepository.get_all_cities(db)

    @staticmethod
    def get_city_by_id(db: Session, city_id: int):
        """Fetches a city by its ID."""
        return CityRepository.get_city_by_id(db, city_id)

    @staticmethod
    def update_city(db: Session, city_id: int, updated_data: dict):
        """Updates a city's details."""
        return CityRepository.update_city(db, city_id, updated_data)

    @staticmethod
    def delete_city(db: Session, city_id: int):
        """Deletes a city by ID."""
        return CityRepository.delete_city(db, city_id)

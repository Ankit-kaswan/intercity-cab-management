from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.cab_repository import CabRepository
from app.services.city_service import CityService
from app.schemas import CabCreate
from app.models import Cab
from sqlalchemy.exc import SQLAlchemyError


class CabService:
    @staticmethod
    def register_cab(db: Session, cab_data: CabCreate) -> Cab:
        """Registers a new cab and logs initial history."""
        try:
            city = CityService.get_city_by_id(db, cab_data.current_city_id)
            if not city:
                raise HTTPException(status_code=400, detail="Invalid city ID: City does not exist.")

            cab = CabRepository.create_cab(db, cab_data.model_dump())

            # Log initial cab state in history
            CabRepository.create_cab_history(db, cab.id, cab.state)

            return cab
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error registering cab: {str(e)}")

    @staticmethod
    def change_cab_location(db: Session, cab_id: int, city_id: int) -> Cab:
        """Changes a cab's location (city)."""
        cab = CabRepository.update_cab_location(db, cab_id, city_id)
        if not cab:
            raise HTTPException(status_code=404, detail="Cab not found")
        return cab

    @staticmethod
    def update_cab_state(db: Session, cab_id: int, new_state: str) -> Cab:
        """Updates a cab's state (Idle, On Trip, etc.)."""
        cab = CabRepository.update_cab_state(db, cab_id, new_state)
        if not cab:
            raise HTTPException(status_code=404, detail="Cab not found")

        # Log initial cab state in history
        CabRepository.create_cab_history(db, cab.id, cab.state)
        return cab

    @staticmethod
    def get_available_cabs(db: Session, city_id: int) -> list[Cab]:
        """Finds available cabs in a city."""
        available_cabs = CabRepository.get_available_cabs(db, city_id)
        if not available_cabs:
            raise HTTPException(status_code=404, detail="No available cabs found")
        return available_cabs

    @staticmethod
    def get_cab_history(db: Session, cab_id: int):
        """Gets cab history from repository."""
        history = CabRepository.get_cab_history(db, cab_id)
        if not history:
            raise HTTPException(status_code=404, detail="No history found for this cab")
        return history

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.schemas import CityCreate, CityResponse
from app.services.city_service import CityService


router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("/", response_model=CityResponse, status_code=status.HTTP_201_CREATED)
def register_city(city_data: CityCreate, db: Session = Depends(get_db)):
    """Registers a new city, handling duplicate city errors."""
    try:
        city = CityService.register_city(db, city_data)
        if not city:
            raise HTTPException(status_code=500, detail="Failed to register city.")
        return city
    except IntegrityError:
        db.rollback()  # Rollback the transaction
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City with this name already exists."
        )


@router.get("/", response_model=list[CityResponse])
def get_all_cities(db: Session = Depends(get_db)):
    """Retrieves all registered cities."""
    return CityService.get_all_cities(db)


@router.get("/{city_id}", response_model=CityResponse)
def get_city_by_id(city_id: int, db: Session = Depends(get_db)):
    """Fetches a city by its ID."""
    city = CityService.get_city_by_id(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/{city_id}", response_model=CityResponse)
def update_city(city_id: int, updated_data: CityCreate, db: Session = Depends(get_db)):
    """Updates city details."""
    updated_city = CityService.update_city(db, city_id, updated_data.dict())
    if not updated_city:
        raise HTTPException(status_code=404, detail="City not found")
    return updated_city


@router.delete("/{city_id}", response_model=dict)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    """Deletes a city by ID."""
    deleted = CityService.delete_city(db, city_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="City not found")
    return {"message": "City deleted successfully"}

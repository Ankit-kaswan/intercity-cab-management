from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import CabCreate, CabResponse, CabHistoryResponse
from app.services.cab_service import CabService
from app.state_machine import CabState

router = APIRouter(prefix="/cabs", tags=["Cabs"])


@router.post("/", response_model=CabResponse, status_code=status.HTTP_201_CREATED)
def register_cab(cab_data: CabCreate, db: Session = Depends(get_db)):
    """Registers a new cab."""
    return CabService.register_cab(db, cab_data)


@router.put("/{cab_id}/location/{city_id}", response_model=CabResponse)
def update_cab_location(cab_id: int, city_id: int, db: Session = Depends(get_db)):
    """Updates a cab's city location."""
    cab = CabService.change_cab_location(db, cab_id, city_id)
    if not cab:
        raise HTTPException(status_code=404, detail="Cab not found")
    return cab


@router.put("/{cab_id}/state/{new_state}", response_model=CabResponse)
def update_cab_state(cab_id: int, new_state: CabState, db: Session = Depends(get_db)):
    """Updates a cab's state (Idle, On Trip, etc.) using Enum choices."""

    cab = CabService.update_cab_state(db, cab_id, new_state.value)
    if not cab:
        raise HTTPException(status_code=404, detail="Cab not found")
    return cab


@router.get("/available/{city_id}", response_model=list[CabResponse])
def get_available_cabs(city_id: int, db: Session = Depends(get_db)):
    """Fetches available cabs in a city."""
    return CabService.get_available_cabs(db, city_id)


@router.get("/{cab_id}/history", response_model=list[CabHistoryResponse])
def get_cab_history(cab_id: int, db: Session = Depends(get_db)):
    """Fetches the history of state changes for a cab."""
    return CabService.get_cab_history(db, cab_id)

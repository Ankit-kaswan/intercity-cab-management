from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.state_machine import CabState
from app.models import Cab, CabHistory


class CabRepository:
    @staticmethod
    def create_cab(db: Session, cab_data: dict) -> Cab:
        """Creates a new cab and persists it in the database."""
        try:
            cab = Cab(**cab_data)
            db.add(cab)
            db.commit()
            db.refresh(cab)
            return cab
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def update_cab_location(db: Session, cab_id: int, city_id: int) -> Cab:
        """Updates the cab's location."""
        cab = db.query(Cab).filter(Cab.id == cab_id).first()
        if not cab:
            raise HTTPException(status_code=404, detail="Cab not found")
        cab.current_city_id = city_id
        db.commit()
        db.refresh(cab)
        return cab

    @staticmethod
    def update_cab_state(db: Session, cab_id: int, new_state: str) -> Cab:
        """Updates cab state, tracks history, and updates last_idle_time if needed."""
        cab = db.query(Cab).filter(Cab.id == cab_id).first()
        if not cab:
            raise HTTPException(status_code=404, detail="Cab not found")

        print(new_state)

        if new_state == CabState.IDLE.value:
            cab.last_idle_time = datetime.utcnow()

        cab.state = new_state
        db.commit()
        db.refresh(cab)

        return cab

    @staticmethod
    def get_available_cabs(db: Session, city_id: int, limit: Optional[int] = None):
        """
        Fetches available cabs in a city, prioritizing the longest idle time.
        Uses:
        - ORDER BY last_idle_time (database-side sorting)
        - FOR UPDATE SKIP LOCKED (prevents multiple bookings on the same cab)
        - LIMIT (reduces load when multiple cabs have the same idle time)
        """
        query = (
            db.query(Cab)
            .filter(Cab.current_city_id == city_id, Cab.state == CabState.IDLE)
            .order_by(Cab.last_idle_time.asc().nulls_first())
            .with_for_update(skip_locked=True)
        )

        if limit:
            query = query.limit(limit)

        return query.all()

    @staticmethod
    def create_cab_history(db: Session, cab_id: int, state: str):
        """Logs a cab's state change in cab_history."""
        cab_history = CabHistory(
            cab_id=cab_id,
            state=state,
            timestamp=datetime.utcnow()
        )
        db.add(cab_history)
        db.commit()

    @staticmethod
    def get_cab_history(db: Session, cab_id: int):
        """Fetches cab history sorted by timestamp (latest first)."""
        return db.query(CabHistory).filter(CabHistory.cab_id == cab_id).order_by(CabHistory.timestamp.desc()).all()

    @staticmethod
    def get_idle_time(db: Session, cab_id: int, start_time: datetime, end_time: datetime):
        """
        Calculates total idle time for a cab within a given duration.
        """
        idle_entries = (
            db.query(CabHistory)
            .filter(
                CabHistory.cab_id == cab_id,
                CabHistory.timestamp >= start_time,
                CabHistory.timestamp <= end_time,
            )
            .order_by(CabHistory.timestamp.asc())
            .all()
        )

        total_idle_time = timedelta()
        last_idle_start = None

        # Check the state before `start_time`
        first_state = (
            db.query(CabHistory)
            .filter(
                CabHistory.cab_id == cab_id,
                CabHistory.timestamp < start_time
            )
            .order_by(CabHistory.timestamp.desc())
            .first()
        )

        # If cab was already IDLE at start_time, consider from start_time
        if first_state and first_state.state == CabState.IDLE:
            last_idle_start = start_time

        for entry in idle_entries:
            if entry.state == CabState.IDLE and last_idle_start is None:
                last_idle_start = max(entry.timestamp, start_time)  # Cab went IDLE

            elif entry.state != CabState.IDLE and last_idle_start:
                total_idle_time += entry.timestamp - last_idle_start
                last_idle_start = None

            # If the cab is still IDLE at the end time
        if last_idle_start:
            total_idle_time += end_time - last_idle_start

        return total_idle_time

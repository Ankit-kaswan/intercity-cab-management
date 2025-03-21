from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLAlchemyEnum, Float, func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from app.state_machine import CabState


class Cab(Base):
    __tablename__ = "cabs"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, unique=True, nullable=False)
    current_city_id = Column(Integer, ForeignKey("cities.id"), nullable=True)
    state = Column(SQLAlchemyEnum(CabState), default=CabState.IDLE)
    last_idle_time = Column(DateTime, default=datetime.utcnow)  # Track last idle time

    current_city = relationship("City", back_populates="cabs")
    history = relationship("CabHistory", back_populates="cab", cascade="all, delete-orphan")


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    cabs = relationship("Cab", back_populates="current_city")
    bookings = relationship("Booking", back_populates="city")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    cab_id = Column(Integer, ForeignKey("cabs.id"), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    pickup_time = Column(DateTime, default=datetime.utcnow)
    drop_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    cab = relationship("Cab")
    city = relationship("City", back_populates="bookings")


class CabHistory(Base):
    __tablename__ = "cab_history"

    id = Column(Integer, primary_key=True, index=True)
    cab_id = Column(Integer, ForeignKey("cabs.id"), nullable=False, index=True)
    state = Column(SQLAlchemyEnum(CabState), nullable=False)
    timestamp = Column(DateTime, nullable=False, server_default=func.now(), index=True)

    cab = relationship("Cab", back_populates="history")

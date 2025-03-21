from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.state_machine import CabState


class CityBase(BaseModel):
    name: str = Field(..., example="Delhi")


class CityCreate(CityBase):
    pass


class CityResponse(CityBase):
    id: int

    class Config:
        from_attributes = True


class CabBase(BaseModel):
    plate_number: str = Field(..., example="ABC-1234")
    current_city_id: int


class CabCreate(CabBase):
    pass


class CabResponse(CabBase):
    id: int
    state: CabState
    last_idle_time: datetime

    class Config:
        from_attributes = True


class BookingBase(BaseModel):
    cab_id: int
    city_id: int


class BookingCreate(BookingBase):
    pass


class BookingResponse(BookingBase):
    id: int
    pickup_time: datetime
    drop_time: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CabHistoryBase(BaseModel):
    cab_id: int
    state: CabState
    timestamp: datetime


class CabHistoryResponse(CabHistoryBase):
    id: int

    class Config:
        from_attributes = True

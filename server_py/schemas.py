from typing import List, Union
from datetime import datetime
from pydantic import BaseModel

# Routes
class RouteBase(BaseModel):
    route_id: str
    route_short_name: str = None
    route_long_name: str = None
    route_type: int
    route_text_color: str = None
    agency_id: str = None
    route_color: str = None

    class Config:
        orm_mode = True

class RouteCreate(RouteBase):
    pass


class Route(RouteBase):
    pass

# Shapes
class ShapeBase(BaseModel):
    shape_id: str
    shape_pt_lat: float = None
    shape_pt_lon: float = None
    shape_pt_sequence: int = None
    shape_dist_traveled: float = None

    class Config:
        orm_mode = True

class ShapeCreate(ShapeBase):
    pass

class Shape(ShapeBase):
    pass

# Trips
class TripBase(BaseModel):
    trip_id: str
    trip_headsign: str = None
    route_id: str
    block_id: str = None
    direction_id: int = None
    shape_id: str = None
    service_id: str
    
    class Config:
        orm_mode = True

class TripCreate(TripBase):
    pass

class Trip(TripBase):
    pass

# Stops
class StopBase(BaseModel):
    stop_id: str
    stop_code: str = None
    stop_name: str = None
    stop_desc: str = None
    stop_lat: float = None
    stop_lon: float = None
    parent_station: str = None
    location_type: int = None
    zone_id: str = None

    class Config:
        orm_mode = True

class StopCreate(StopBase):
    pass


class Stop(StopBase):
    pass
    # stop_times: List[StopTime] = []
    # routes: List[Route] = []


# StopTimes
class StopTimeBase(BaseModel):
    trip_id: str
    stop_id: str
    arrival_time: datetime = None
    departure_time: datetime = None
    stop_sequence: int
    stop_headsign: str = None
    pickup_type: int = None
    drop_off_type: int = None
    shape_dist_traveled: float = None

    class Config:
        orm_mode = True
    

class StopTimeCreate(StopTimeBase):
    pass


class StopTime(StopTimeBase):
    pass


# Vehicle Positions
class VehiclePositionBase(BaseModel):
    vehicle_id: str
    vehicle_lat: float
    vehicle_lon: float
    vehicle_bearing: float = None
    vehicle_speed: float = None
    vehicle_timestamp: datetime
    trip_id: str = None
    route_id: str = None
    direction_id: int = None

    class Config:
        orm_mode = True

class VehiclePositionCreate(VehiclePositionBase):
    pass

class VehiclePosition(VehiclePositionBase):
    pass
    # route: Route = None



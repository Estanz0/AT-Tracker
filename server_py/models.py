from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, Table
from sqlalchemy.orm import relationship, backref

from database import Base

class Route(Base):
    __tablename__ = "routes"

    route_id = Column(String, primary_key=True, index=True)
    route_short_name = Column(String)
    route_long_name = Column(String)
    route_type = Column(Integer, nullable=False)
    route_text_color = Column(String)
    agency_id = Column(String)
    route_color = Column(String)

    # stops = relationship("Stop", secondary=route_stop, back_populates="routes")

    # trips = relationship("Trip", backref="routes")

    # vehicle_positions = relationship("VehiclePosition", back_populates="route")

class Shape(Base):
    __tablename__ = "shapes"

    shape_id = Column(String, primary_key=True, index=True)
    shape_pt_lat = Column(Float)
    shape_pt_lon = Column(Float)
    shape_pt_sequence = Column(Integer)
    shape_dist_traveled = Column(Float)

class Trip(Base):
    __tablename__ = "trips"

    trip_id = Column(String, primary_key=True, index=True)
    trip_headsign = Column(String)
    route_id = Column(String, ForeignKey("routes.route_id"), nullable=False)
    block_id = Column(String)
    direction_id = Column(Integer)
    shape_id = Column(String)
    service_id = Column(String, nullable=False)

class Stop(Base):
    __tablename__ = "stops"

    stop_id = Column(String, primary_key=True, index=True)
    stop_code = Column(String)
    stop_name = Column(String)
    stop_desc = Column(String)
    stop_lat = Column(Float)
    stop_lon = Column(Float)
    parent_station = Column(String, ForeignKey("stops.stop_id"))
    location_type = Column(Integer)
    zone_id = Column(String)


    # routes = relationship(
    #     "Route", secondary=route_stop, back_populates="stops"
    # )


class StopTime(Base):
    __tablename__ = "stop_times"

    trip_id = Column(String, ForeignKey("trips.trip_id"), primary_key=True)
    stop_id = Column(String, ForeignKey("stops.stop_id"), primary_key=True)
    arrival_time = Column(DateTime)
    departure_time = Column(DateTime)
    stop_sequence = Column(Integer, nullable=False)
    stop_headsign = Column(String)
    pickup_type = Column(Integer)
    drop_off_type = Column(Integer)
    shape_dist_traveled = Column(Integer)

    # stop = relationship("Stop", back_populates="stop_times") 


class VehiclePosition(Base):
    __tablename__ = "vehicle_positions"

    vehicle_id = Column(String, primary_key=True)
    vehicle_lat = Column(Float, nullable=False)
    vehicle_lon = Column(Float, nullable=False)
    vehicle_bearing = Column(Float)
    vehicle_speed = Column(Float)
    vehicle_timestamp = Column(DateTime)
    trip_id = Column(String, ForeignKey("trips.trip_id"))
    route_id = Column(String, ForeignKey("routes.route_id"))
    direction_id = Column(Integer)

    # route = relationship("Route", back_populates="vehicle_positions") 





    

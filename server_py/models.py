from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, Table
from sqlalchemy.orm import relationship, backref

from database import Base

route_stop = Table(
    "route_stop",
    Base.metadata,
    Column("stop_id", ForeignKey("stops.stop_id"), primary_key=True),
    Column("route_id", ForeignKey("routes.route_id"), primary_key=True),
)

class Stop(Base):
    __tablename__ = "stops"

    stop_id = Column(String, unique=True, index=True, nullable=False)
    stop_code = Column(String, primary_key=True, index=True, nullable=False)
    stop_name = Column(String, nullable=False)
    stop_desc = Column(String)
    stop_lat = Column(Float, nullable=False)
    stop_lon = Column(Float, nullable=False)

    stop_times = relationship("StopTime", backref="stops")

    routes = relationship(
        "Route", secondary=route_stop, back_populates="stops"
    )


class StopTime(Base):
    __tablename__ = "stop_times"

    trip_id = Column(String, primary_key=True)
    arrival_time = Column(DateTime)
    departure_time = Column(DateTime, nullable=False)
    stop_id = Column(String, ForeignKey("stops.stop_id"), primary_key=True)
    stop_sequence = Column(Integer)
    stop_headsign = Column(String)
    pickup_type = Column(Integer)
    drop_off_type = Column(Integer)
    shape_dist_traveled = Column(Integer)

    # stop = relationship("Stop", back_populates="stop_times") 

class Route(Base):
    __tablename__ = "routes"

    route_id = Column(String, primary_key=True, index=True)
    route_long_name = Column(String, nullable=False)
    route_short_name = Column(String, nullable=False)

    stops = relationship("Stop", secondary=route_stop, back_populates="routes")

    trips = relationship("Trip", backref="routes")

    # vehicle_positions = relationship("VehiclePosition", back_populates="route")

class Trip(Base):
    __tablename__ = "trips"

    trip_id = Column(String, primary_key=True, index=True)
    route_id = Column(String, ForeignKey("routes.route_id"))
    service_id = Column(String)
    trip_headsign = Column(String)
    direction_id = Column(Integer)
    shape_id = Column(String)

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





    

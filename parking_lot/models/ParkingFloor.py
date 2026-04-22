import uuid

from parking_lot.enums.VehicleType import VehicleType
from parking_lot.models.BikeParkingSpot import BikeParkingSpot
from parking_lot.models.CarParkingSpot import CarParkingSpot
from parking_lot.models.ParkingSpot import ParkingSpot
from parking_lot.models.TruckParkingSpot import TruckParkingSpot


class ParkingFloor:
    def __init__(self, parking_spots, parking_floor_id):
        self.parking_spots = parking_spots
        self.parking_floor_id = parking_floor_id

    def get_parking_spots(self):
        return self.parking_spots

    def add_parking_spot(self, parking_spot: ParkingSpot):
        self.parking_spots.append(parking_spot)

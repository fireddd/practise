
from abc import ABC, abstractmethod
class ParkingSpot(ABC):
    def __init__(self, vehicle_type, parking_id):
        self.vehicle_type = vehicle_type
        self.parking_id = parking_id
        self.is_occupied = False
    def occupy(self):
        self.is_occupied = True
        print(self.parking_id, " is occupied")

    def mark_free(self):
        self.is_occupied = False
        print(self.parking_id, " is free now")

    def __repr__(self):
        return str(self.vehicle_type)+ str(self.parking_id) + " " + str(self.is_occupied)
from abc import ABC, abstractmethod

from parking_lot.service.ParkingFloorService import ParkingFloorService


class ParkingStrategy(ABC):
    @abstractmethod
    def get_parking_floors(self, parking_floors, vehicle_type):
        pass

class ClosestParkingFloor(ParkingStrategy):
    def get_parking_floors(self, parking_floors, vehicle_type):
        for parking_floor in parking_floors:
            possible = parking_floor.get_free_parking_spot_by_vehicle_type(vehicle_type)
            if len(possible) > 0:
                return parking_floor
        raise ValueError("No parking spots for", vehicle_type)

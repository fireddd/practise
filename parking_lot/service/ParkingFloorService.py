import uuid

from parking_lot.models.ParkingFloor import ParkingFloor
import uuid


from parking_lot.enums.VehicleType import VehicleType
from parking_lot.models.BikeParkingSpot import BikeParkingSpot
from parking_lot.models.CarParkingSpot import CarParkingSpot
from parking_lot.models.TruckParkingSpot import TruckParkingSpot


class ParkingFloorService:
    def __init__(self, parking_floor: ParkingFloor):
        self.parking_floor = parking_floor
    def get_free_slots(self):
        return self.get_parking_free_spots()
    def get_occupied_slots(self):
        return self.get_parking_occupied_spots()
    def mark_free(self, slot_id):
        self.mark_parking_spot_available(slot_id)
    def mark_occupied(self, slot_id):
        self.mark_parking_spot_occupied(slot_id)
    def get_parking_free_spots(self):
        result = []
        for spot in self.parking_floor.parking_spots:
            if spot.is_occupied == False:
                result.append(spot)
        return result

    def get_parking_occupied_spots(self):
        result = []
        for spot in self.parking_floor.parking_spots:
            if spot.is_occupied == True:
                result.append(spot)
        return result

    def get_parking_spot_by_id(self, parking_spot_id):
        for spot in self.parking_floor.parking_spots:
            if spot.parking_id == parking_spot_id:
                return spot
        raise ValueError("Invalid parking spot ID")

    def get_free_parking_spot_by_vehicle_type(self, vehicle_type):
        result = []
        for spot in self.parking_floor.parking_spots:
            if spot.vehicle_type == vehicle_type and spot.is_occupied == False:
                result.append(spot)
        return result

    def mark_parking_spot_available(self, parking_spot_id):
        for spot in self.parking_floor.parking_spots:
            if spot.parking_id == parking_spot_id:
                spot.is_occupied = False
                return True
        return False

    def mark_parking_spot_occupied(self, parking_spot_id):
        for spot in self.parking_floor.parking_spots:
            if spot.parking_id == parking_spot_id:
                spot.is_occupied = True
                return True
        return False

    def park(self, vehicle_type):
        possible_nodes = self.get_free_parking_spot_by_vehicle_type(vehicle_type)
        if len(possible_nodes) == 0:
            raise  ValueError("No slots avalibale")
        curr = possible_nodes[0]
        self.mark_parking_spot_occupied(curr.parking_id)
        print(vehicle_type," is parked")
        return curr

    def unpark(self, parking_spot_id):
        print(parking_spot_id," is unparked")
        self.mark_parking_spot_available(parking_spot_id)

    def add_parking_slot(self, vehicleType):
        parking_spot_id = uuid.uuid4()
        match vehicleType:
            case VehicleType.CAR:
                curr = CarParkingSpot(parking_spot_id)
                self.parking_floor.add_parking_spot(curr)
            case VehicleType.BIKE:
                curr = BikeParkingSpot(parking_spot_id)
                self.parking_floor.add_parking_spot(curr)
            case VehicleType.TRUCK:
                curr = TruckParkingSpot(parking_spot_id)
                self.parking_floor.add_parking_spot(curr)
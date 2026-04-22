from parking_lot.enums.VehicleType import VehicleType
from parking_lot.models.ParkingSpot import ParkingSpot


class BikeParkingSpot(ParkingSpot):
    def __init__(self, parking_spot_id):
        super().__init__(VehicleType.BIKE, parking_spot_id)
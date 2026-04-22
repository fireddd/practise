import uuid
from math import floor

from parking_lot.daos.InMemoryTicketDao import InMemoryTicketDao
from parking_lot.models.Ticket import Ticket
from parking_lot.parkingstrategy.ParkingStrategy import ClosestParkingFloor


class ParkingLotService:
    def __init__(self, parking_floors, parking_strategy, parking_lot_id):
        self.parking_floors = parking_floors
        self.parking_strategy = parking_strategy
        self.parking_lot_id = parking_lot_id
        self.ticket_dao = InMemoryTicketDao()

    def get_parking_free_spots(self):
        result = []
        for parking_floor in self.parking_floors:
            result.extend(parking_floor.get_parking_free_spots())
        return result

    def get_parking_occupied_spots(self):
        result = []
        for parking_floor in self.parking_floors:
            result.extend(parking_floor.get_parking_occupied_spots())
        return result

    def get_parking_occupied_spots_by_vehicle_type(self, vehicle_type):
        all_spots = self.get_parking_occupied_spots()
        result = []
        for spot in all_spots:
            if spot.vehicle_type == vehicle_type:
                result.append(spot)
        return result

    def get_parking_free_spots_by_vehicle_type(self, vehicle_type):
        all_spots = self.get_parking_free_spots()
        result = []
        for spot in all_spots:
            if spot.vehicle_type == vehicle_type:
                result.append(spot)
        return result

    def park(self, vehicle_type):
        avaliable_parking_floor = self.parking_strategy.get_parking_floors(self.parking_floors, vehicle_type)
        spot = avaliable_parking_floor.park(vehicle_type)
        ticket_id = uuid.uuid4()
        t = Ticket(self.parking_lot_id, avaliable_parking_floor.parking_floor.parking_floor_id, spot.parking_id, ticket_id)
        self.ticket_dao.save_ticket(t, ticket_id)
        return t

    def unpark(self, ticket):
        for parking_floor in self.parking_floors:
            if parking_floor.parking_floor.parking_floor_id == ticket.floor_number:
                parking_floor.unpark(ticket.slot_number)


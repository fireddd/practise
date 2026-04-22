class Ticket:
    def __init__(self, parking_lot_id, floor_number, slot_number, ticket_id):
        self.parking_lot_id = parking_lot_id
        self.floor_number = floor_number
        self.slot_number = slot_number
        self.ticket_id = ticket_id

    def __repr__(self):
        return f'{self.parking_lot_id} {self.floor_number} {self.slot_number} {self.ticket_id}'

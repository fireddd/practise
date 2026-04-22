
from parking_lot.daos.ITicketDao import ITicketDao


class InMemoryTicketDao(ITicketDao):
    def __init__(self):
        self.tickets = {}
    def save_ticket(self, ticket, ticket_id):
        self.tickets[ticket_id] = ticket
        return ticket_id

    def get_ticket(self, ticket_id):
        if ticket_id not in self.tickets.keys():
            raise KeyError("Ticket {} not found.".format(ticket_id))
        return self.tickets[ticket_id]

    def get_all_tickets(self):
        return self.tickets.values()
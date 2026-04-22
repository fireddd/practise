from abc import ABC, abstractmethod

class ITicketDao(ABC):
    @abstractmethod
    def save_ticket(self, ticket, ticket_id):
        pass

    @abstractmethod
    def get_ticket(self, ticket_id):
        pass

    @abstractmethod
    def get_all_tickets(self):
        pass
import uuid

from models import User
from exceptions import UserNotFoundException


class UserService:
    def __init__(self):
        self._users = {}

    def create_user(self, name, tier):
        user_id = str(uuid.uuid4())[:8]
        user = User(user_id, name, tier)
        self._users[user_id] = user
        return user

    def get_user(self, user_id):
        if user_id not in self._users:
            raise UserNotFoundException(f"User '{user_id}' not found")
        return self._users[user_id]

from enums.marker import Marker


class Player:
    def __init__(self, name: str, marker: Marker):
        self._name = name
        self._marker = marker

    @property
    def name(self) -> str:
        return self._name

    @property
    def marker(self) -> Marker:
        return self._marker

    def __str__(self) -> str:
        return f"{self._name} ({self._marker.value})"

from dataclasses import dataclass

from tic_tac_toe.marker import Marker


@dataclass(frozen=True)
class Player:
    name: str
    marker: Marker


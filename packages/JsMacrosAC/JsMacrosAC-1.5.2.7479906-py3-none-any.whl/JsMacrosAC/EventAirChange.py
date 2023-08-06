from typing import overload
from .BaseEvent import BaseEvent


class EventAirChange(BaseEvent):
	air: int

	@overload
	def __init__(self, air: int) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



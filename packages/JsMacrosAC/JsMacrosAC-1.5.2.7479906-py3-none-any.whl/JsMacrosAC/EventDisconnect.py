from typing import overload
from .BaseEvent import BaseEvent


class EventDisconnect(BaseEvent):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



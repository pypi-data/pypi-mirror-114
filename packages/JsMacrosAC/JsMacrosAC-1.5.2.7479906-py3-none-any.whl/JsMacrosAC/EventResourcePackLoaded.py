from typing import overload
from typing import List
from .BaseEvent import BaseEvent


class EventResourcePackLoaded(BaseEvent):
	isGameStart: bool
	loadedPacks: List[str]

	@overload
	def __init__(self, isGameStart: bool) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



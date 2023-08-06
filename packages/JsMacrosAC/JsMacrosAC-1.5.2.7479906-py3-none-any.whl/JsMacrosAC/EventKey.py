from typing import overload
from .BaseEvent import BaseEvent


class EventKey(BaseEvent):
	action: int
	key: str
	mods: str

	@overload
	def __init__(self, key: int, scancode: int, action: int, mods: int) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	@overload
	def getKeyModifiers(self, mods: int) -> str:
		pass

	@overload
	def getModInt(self, mods: str) -> int:
		pass

	pass



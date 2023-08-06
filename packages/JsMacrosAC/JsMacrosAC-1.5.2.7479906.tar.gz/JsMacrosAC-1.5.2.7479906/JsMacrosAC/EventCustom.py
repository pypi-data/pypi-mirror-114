from typing import overload
from .BaseEvent import BaseEvent
from .MethodWrapper import MethodWrapper


class EventCustom(BaseEvent):
	eventName: str

	@overload
	def __init__(self, eventName: str) -> None:
		pass

	@overload
	def trigger(self) -> None:
		pass

	@overload
	def trigger(self, callback: MethodWrapper) -> None:
		pass

	@overload
	def triggerJoin(self) -> None:
		pass

	@overload
	def putInt(self, name: str, i: int) -> int:
		pass

	@overload
	def putString(self, name: str, str: str) -> str:
		pass

	@overload
	def putDouble(self, name: str, d: float) -> float:
		pass

	@overload
	def putBoolean(self, name: str, b: bool) -> bool:
		pass

	@overload
	def putObject(self, name: str, o: object) -> object:
		pass

	@overload
	def getType(self, name: str) -> str:
		pass

	@overload
	def getInt(self, name: str) -> int:
		pass

	@overload
	def getString(self, name: str) -> str:
		pass

	@overload
	def getDouble(self, name: str) -> float:
		pass

	@overload
	def getBoolean(self, name: str) -> bool:
		pass

	@overload
	def getObject(self, name: str) -> object:
		pass

	@overload
	def registerEvent(self) -> None:
		pass

	pass



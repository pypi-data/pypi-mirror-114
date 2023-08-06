from typing import overload
from .BaseEvent import BaseEvent
from .BaseProfile import BaseProfile


class EventProfileLoad(BaseEvent):
	profileName: str

	@overload
	def __init__(self, profile: BaseProfile, profileName: str) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



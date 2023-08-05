from typing import overload
from typing import List
from typing import TypeVar
from .BaseEvent import *

List = TypeVar["java.util.List_java.lang.String_"]

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



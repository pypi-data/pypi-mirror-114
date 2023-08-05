from typing import overload
from typing import List
from typing import TypeVar
from .BaseEvent import *
from .PositionCommon_Pos3D import *

List = TypeVar["java.util.List_java.lang.String_"]

class EventSignEdit(BaseEvent):
	pos: PositionCommon_Pos3D
	closeScreen: bool
	signText: List[str]

	@overload
	def __init__(self, signText: List[str], x: int, y: int, z: int) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



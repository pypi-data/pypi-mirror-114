from typing import overload
from .BaseEvent import BaseEvent
from .PositionCommon_Pos3D import PositionCommon_Pos3D


class EventSound(BaseEvent):
	sound: str
	volume: float
	pitch: float
	position: PositionCommon_Pos3D

	@overload
	def __init__(self, sound: str, volume: float, pitch: float, x: float, y: float, z: float) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



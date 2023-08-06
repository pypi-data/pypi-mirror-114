from typing import overload
from .PositionCommon_Pos3D import PositionCommon_Pos3D
from .PositionCommon_Vec2D import PositionCommon_Vec2D


class PositionCommon_Pos2D:
	ZERO: "PositionCommon_Pos2D"
	x: float
	y: float

	@overload
	def __init__(self, x: float, y: float) -> None:
		pass

	@overload
	def getX(self) -> float:
		pass

	@overload
	def getY(self) -> float:
		pass

	@overload
	def add(self, pos: "PositionCommon_Pos2D") -> "PositionCommon_Pos2D":
		pass

	@overload
	def multiply(self, pos: "PositionCommon_Pos2D") -> "PositionCommon_Pos2D":
		pass

	@overload
	def toString(self) -> str:
		pass

	@overload
	def to3D(self) -> PositionCommon_Pos3D:
		pass

	@overload
	def toVector(self) -> PositionCommon_Vec2D:
		pass

	pass



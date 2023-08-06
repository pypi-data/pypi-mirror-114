from typing import overload
from .PositionCommon_Pos2D import PositionCommon_Pos2D
from .PositionCommon_Vec3D import PositionCommon_Vec3D


class PositionCommon_Vec2D:
	x1: float
	y1: float
	x2: float
	y2: float

	@overload
	def __init__(self, x1: float, y1: float, x2: float, y2: float) -> None:
		pass

	@overload
	def __init__(self, start: PositionCommon_Pos2D, end: PositionCommon_Pos2D) -> None:
		pass

	@overload
	def getX1(self) -> float:
		pass

	@overload
	def getY1(self) -> float:
		pass

	@overload
	def getX2(self) -> float:
		pass

	@overload
	def getY2(self) -> float:
		pass

	@overload
	def getDeltaX(self) -> float:
		pass

	@overload
	def getDeltaY(self) -> float:
		pass

	@overload
	def getStart(self) -> PositionCommon_Pos2D:
		pass

	@overload
	def getEnd(self) -> PositionCommon_Pos2D:
		pass

	@overload
	def getMagnitude(self) -> float:
		pass

	@overload
	def add(self, vec: "PositionCommon_Vec2D") -> "PositionCommon_Vec2D":
		pass

	@overload
	def multiply(self, vec: "PositionCommon_Vec2D") -> "PositionCommon_Vec2D":
		pass

	@overload
	def dotProduct(self, vec: "PositionCommon_Vec2D") -> float:
		pass

	@overload
	def reverse(self) -> "PositionCommon_Vec2D":
		pass

	@overload
	def toString(self) -> str:
		pass

	@overload
	def to3D(self) -> PositionCommon_Vec3D:
		pass

	pass



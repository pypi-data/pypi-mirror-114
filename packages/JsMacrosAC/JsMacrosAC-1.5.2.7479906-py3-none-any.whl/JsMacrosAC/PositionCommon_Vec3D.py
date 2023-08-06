from typing import overload
from .PositionCommon_Vec2D import PositionCommon_Vec2D
from .PositionCommon_Pos3D import PositionCommon_Pos3D


class PositionCommon_Vec3D(PositionCommon_Vec2D):
	z1: float
	z2: float

	@overload
	def __init__(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> None:
		pass

	@overload
	def __init__(self, start: PositionCommon_Pos3D, end: PositionCommon_Pos3D) -> None:
		pass

	@overload
	def getZ1(self) -> float:
		pass

	@overload
	def getZ2(self) -> float:
		pass

	@overload
	def getDeltaZ(self) -> float:
		pass

	@overload
	def getStart(self) -> PositionCommon_Pos3D:
		pass

	@overload
	def getEnd(self) -> PositionCommon_Pos3D:
		pass

	@overload
	def getMagnitude(self) -> float:
		pass

	@overload
	def add(self, vec: "PositionCommon_Vec3D") -> "PositionCommon_Vec3D":
		pass

	@overload
	def multiply(self, vec: "PositionCommon_Vec3D") -> "PositionCommon_Vec3D":
		pass

	@overload
	def getPitch(self) -> float:
		pass

	@overload
	def getYaw(self) -> float:
		pass

	@overload
	def dotProduct(self, vec: "PositionCommon_Vec3D") -> float:
		pass

	@overload
	def crossProduct(self, vec: "PositionCommon_Vec3D") -> "PositionCommon_Vec3D":
		pass

	@overload
	def reverse(self) -> "PositionCommon_Vec3D":
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



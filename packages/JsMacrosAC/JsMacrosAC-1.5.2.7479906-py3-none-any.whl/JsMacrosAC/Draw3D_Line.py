from typing import overload
from typing import TypeVar
from .PositionCommon_Vec3D import PositionCommon_Vec3D

MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]

class Draw3D_Line:
	pos: PositionCommon_Vec3D
	color: int
	cull: bool

	@overload
	def __init__(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, color: int, cull: bool) -> None:
		pass

	@overload
	def __init__(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, color: int, alpha: int, cull: bool) -> None:
		pass

	@overload
	def setPos(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> None:
		pass

	@overload
	def setColor(self, color: int) -> None:
		pass

	@overload
	def setColor(self, color: int, alpha: int) -> None:
		pass

	@overload
	def setAlpha(self, alpha: int) -> None:
		pass

	@overload
	def render(self, matrixStack: MatrixStack) -> None:
		pass

	pass



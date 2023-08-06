from typing import overload
from typing import List
from typing import TypeVar
from .Draw3D_Box import Draw3D_Box
from .Draw3D_Line import Draw3D_Line
from .PositionCommon_Pos3D import PositionCommon_Pos3D

MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]

class Draw3D:

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def getBoxes(self) -> List[Draw3D_Box]:
		pass

	@overload
	def getLines(self) -> List[Draw3D_Line]:
		pass

	@overload
	def addBox(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, color: int, fillColor: int, fill: bool) -> Draw3D_Box:
		pass

	@overload
	def addBox(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, color: int, fillColor: int, fill: bool, cull: bool) -> Draw3D_Box:
		pass

	@overload
	def addBox(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, color: int, alpha: int, fillColor: int, fillAlpha: int, fill: bool) -> Draw3D_Box:
		pass

	@overload
	def addBox(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, color: int, alpha: int, fillColor: int, fillAlpha: int, fill: bool, cull: bool) -> Draw3D_Box:
		pass

	@overload
	def removeBox(self, b: Draw3D_Box) -> "Draw3D":
		pass

	@overload
	def addLine(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, color: int) -> Draw3D_Line:
		pass

	@overload
	def addLine(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, color: int, cull: bool) -> Draw3D_Line:
		pass

	@overload
	def addLine(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, color: int, alpha: int) -> Draw3D_Line:
		pass

	@overload
	def addLine(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, color: int, alpha: int, cull: bool) -> Draw3D_Line:
		pass

	@overload
	def removeLine(self, l: Draw3D_Line) -> "Draw3D":
		pass

	@overload
	def addPoint(self, point: PositionCommon_Pos3D, radius: float, color: int) -> Draw3D_Box:
		pass

	@overload
	def addPoint(self, x: float, y: float, z: float, radius: float, color: int) -> Draw3D_Box:
		pass

	@overload
	def addPoint(self, x: float, y: float, z: float, radius: float, color: int, alpha: int, cull: bool) -> Draw3D_Box:
		pass

	@overload
	def render(self, matrixStack: MatrixStack) -> None:
		pass

	pass



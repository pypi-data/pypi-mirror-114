from typing import overload
from typing import List
from typing import TypeVar
from .Draw3D_Box import *
from .Draw3D_Line import *
from .Draw3D import *
from .PositionCommon_Pos3D import *

MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]
List = TypeVar["java.util.List_xyz.wagyourtail.jsmacros.client.api.classes.Draw3D.Line_"]

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



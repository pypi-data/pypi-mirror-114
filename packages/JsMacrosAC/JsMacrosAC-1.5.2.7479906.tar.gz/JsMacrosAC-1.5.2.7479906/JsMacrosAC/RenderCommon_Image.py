from typing import overload
from typing import TypeVar
from .RenderCommon_RenderElement import RenderCommon_RenderElement

MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]

class RenderCommon_Image(RenderCommon_RenderElement):
	rotation: float
	x: int
	y: int
	width: int
	height: int
	imageX: int
	imageY: int
	regionWidth: int
	regionHeight: int
	textureWidth: int
	textureHeight: int
	zIndex: int

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, zIndex: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int, rotation: float) -> None:
		pass

	@overload
	def setPos(self, x: int, y: int, width: int, height: int) -> None:
		pass

	@overload
	def setRotation(self, rotation: float) -> "RenderCommon_Image":
		pass

	@overload
	def setImage(self, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int) -> None:
		pass

	@overload
	def getImage(self) -> str:
		pass

	@overload
	def render(self, matrices: MatrixStack, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	@overload
	def getZIndex(self) -> int:
		pass

	pass



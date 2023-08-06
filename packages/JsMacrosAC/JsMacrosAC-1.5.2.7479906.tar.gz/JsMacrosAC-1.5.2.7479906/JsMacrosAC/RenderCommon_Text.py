from typing import overload
from typing import TypeVar
from .RenderCommon_RenderElement import RenderCommon_RenderElement
from .TextHelper import TextHelper

MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]
Text = TypeVar["net.minecraft.text.Text"]

class RenderCommon_Text(RenderCommon_RenderElement):
	text: Text
	scale: float
	rotation: float
	x: int
	y: int
	color: int
	width: int
	shadow: bool
	zIndex: int

	@overload
	def __init__(self, text: str, x: int, y: int, color: int, zIndex: int, shadow: bool, scale: float, rotation: float) -> None:
		pass

	@overload
	def __init__(self, text: TextHelper, x: int, y: int, color: int, zIndex: int, shadow: bool, scale: float, rotation: float) -> None:
		pass

	@overload
	def setScale(self, scale: float) -> "RenderCommon_Text":
		pass

	@overload
	def setRotation(self, rotation: float) -> "RenderCommon_Text":
		pass

	@overload
	def setPos(self, x: int, y: int) -> "RenderCommon_Text":
		pass

	@overload
	def setText(self, text: str) -> "RenderCommon_Text":
		pass

	@overload
	def setText(self, text: TextHelper) -> "RenderCommon_Text":
		pass

	@overload
	def getText(self) -> TextHelper:
		pass

	@overload
	def getWidth(self) -> int:
		pass

	@overload
	def render(self, matrices: MatrixStack, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	@overload
	def getZIndex(self) -> int:
		pass

	pass



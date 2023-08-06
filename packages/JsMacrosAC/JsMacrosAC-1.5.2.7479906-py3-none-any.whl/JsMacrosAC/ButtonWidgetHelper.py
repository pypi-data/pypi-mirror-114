from typing import overload
from typing import TypeVar
from typing import Generic
from .RenderCommon_RenderElement import RenderCommon_RenderElement
from .BaseHelper import BaseHelper
from .TextHelper import TextHelper

T = TypeVar("T")
MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]

class ButtonWidgetHelper(RenderCommon_RenderElement, Generic[T], BaseHelper):
	zIndex: int

	@overload
	def __init__(self, btn: T) -> None:
		pass

	@overload
	def __init__(self, btn: T, zIndex: int) -> None:
		pass

	@overload
	def getX(self) -> int:
		pass

	@overload
	def getY(self) -> int:
		pass

	@overload
	def setPos(self, x: int, y: int) -> "ButtonWidgetHelper":
		pass

	@overload
	def getWidth(self) -> int:
		pass

	@overload
	def setLabel(self, label: str) -> "ButtonWidgetHelper":
		pass

	@overload
	def setLabel(self, helper: TextHelper) -> "ButtonWidgetHelper":
		pass

	@overload
	def getLabel(self) -> TextHelper:
		pass

	@overload
	def getActive(self) -> bool:
		pass

	@overload
	def setActive(self, t: bool) -> "ButtonWidgetHelper":
		pass

	@overload
	def setWidth(self, width: int) -> "ButtonWidgetHelper":
		pass

	@overload
	def click(self) -> "ButtonWidgetHelper":
		pass

	@overload
	def click(self, await: bool) -> "ButtonWidgetHelper":
		pass

	@overload
	def render(self, matrices: MatrixStack, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	@overload
	def getZIndex(self) -> int:
		pass

	pass



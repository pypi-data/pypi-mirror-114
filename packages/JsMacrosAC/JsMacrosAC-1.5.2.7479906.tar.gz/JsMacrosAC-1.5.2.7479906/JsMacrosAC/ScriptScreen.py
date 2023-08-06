from typing import overload
from typing import TypeVar
from .BaseScreen import BaseScreen
from .IScreen import IScreen
from .MethodWrapper import MethodWrapper

MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]

class ScriptScreen(BaseScreen):

	@overload
	def __init__(self, title: str, dirt: bool) -> None:
		pass

	@overload
	def setParent(self, parent: IScreen) -> None:
		pass

	@overload
	def setOnRender(self, onRender: MethodWrapper) -> None:
		pass

	@overload
	def render(self, matrices: MatrixStack, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	@overload
	def onClose(self) -> None:
		pass

	pass



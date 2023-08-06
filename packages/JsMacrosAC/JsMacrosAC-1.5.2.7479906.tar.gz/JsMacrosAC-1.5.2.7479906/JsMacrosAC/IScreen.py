from typing import overload
from typing import List
from typing import TypeVar
from .IDraw2D import IDraw2D
from .ButtonWidgetHelper import ButtonWidgetHelper
from .TextFieldWidgetHelper import TextFieldWidgetHelper
from .MethodWrapper import MethodWrapper
from .RenderCommon_Rect import RenderCommon_Rect
from .RenderCommon_Item import RenderCommon_Item
from .ItemStackHelper import ItemStackHelper

MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]

class IScreen(IDraw2D):

	@overload
	def getScreenClassName(self) -> str:
		pass

	@overload
	def getTitleText(self) -> str:
		pass

	@overload
	def getButtonWidgets(self) -> List[ButtonWidgetHelper]:
		pass

	@overload
	def getTextFields(self) -> List[TextFieldWidgetHelper]:
		pass

	@overload
	def addButton(self, x: int, y: int, width: int, height: int, text: str, callback: MethodWrapper) -> ButtonWidgetHelper:
		pass

	@overload
	def addButton(self, x: int, y: int, width: int, height: int, zIndex: int, text: str, callback: MethodWrapper) -> ButtonWidgetHelper:
		pass

	@overload
	def removeButton(self, btn: ButtonWidgetHelper) -> "IScreen":
		pass

	@overload
	def addTextInput(self, x: int, y: int, width: int, height: int, message: str, onChange: MethodWrapper) -> TextFieldWidgetHelper:
		pass

	@overload
	def addTextInput(self, x: int, y: int, width: int, height: int, zIndex: int, message: str, onChange: MethodWrapper) -> TextFieldWidgetHelper:
		pass

	@overload
	def removeTextInput(self, inp: TextFieldWidgetHelper) -> "IScreen":
		pass

	@overload
	def setOnMouseDown(self, onMouseDown: MethodWrapper) -> "IScreen":
		pass

	@overload
	def setOnMouseDrag(self, onMouseDrag: MethodWrapper) -> "IScreen":
		pass

	@overload
	def setOnMouseUp(self, onMouseUp: MethodWrapper) -> "IScreen":
		pass

	@overload
	def setOnScroll(self, onScroll: MethodWrapper) -> "IScreen":
		pass

	@overload
	def setOnKeyPressed(self, onKeyPressed: MethodWrapper) -> "IScreen":
		pass

	@overload
	def setOnClose(self, onClose: MethodWrapper) -> "IScreen":
		pass

	@overload
	def close(self) -> None:
		pass

	@overload
	def addRect(self, x1: int, y1: int, x2: int, y2: int, color: int) -> RenderCommon_Rect:
		pass

	@overload
	def addRect(self, x1: int, y1: int, x2: int, y2: int, color: int, alpha: int) -> RenderCommon_Rect:
		pass

	@overload
	def addRect(self, x1: int, y1: int, x2: int, y2: int, color: int, alpha: int, rotation: float) -> RenderCommon_Rect:
		pass

	@overload
	def removeRect(self, r: RenderCommon_Rect) -> "IScreen":
		pass

	@overload
	def addItem(self, x: int, y: int, id: str) -> RenderCommon_Item:
		pass

	@overload
	def addItem(self, x: int, y: int, id: str, overlay: bool) -> RenderCommon_Item:
		pass

	@overload
	def addItem(self, x: int, y: int, id: str, overlay: bool, scale: float, rotation: float) -> RenderCommon_Item:
		pass

	@overload
	def addItem(self, x: int, y: int, item: ItemStackHelper) -> RenderCommon_Item:
		pass

	@overload
	def addItem(self, x: int, y: int, item: ItemStackHelper, overlay: bool) -> RenderCommon_Item:
		pass

	@overload
	def addItem(self, x: int, y: int, item: ItemStackHelper, overlay: bool, scale: float, rotation: float) -> RenderCommon_Item:
		pass

	@overload
	def removeItem(self, i: RenderCommon_Item) -> "IScreen":
		pass

	@overload
	def reloadScreen(self) -> "IScreen":
		pass

	@overload
	def onRenderInternal(self, matrices: MatrixStack, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass



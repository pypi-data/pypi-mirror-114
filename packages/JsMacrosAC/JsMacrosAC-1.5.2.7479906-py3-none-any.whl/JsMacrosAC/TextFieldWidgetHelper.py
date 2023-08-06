from typing import overload
from typing import TypeVar
from .ButtonWidgetHelper import ButtonWidgetHelper

TextFieldWidget = TypeVar["net.minecraft.client.gui.widget.TextFieldWidget"]

class TextFieldWidgetHelper(ButtonWidgetHelper):

	@overload
	def __init__(self, t: TextFieldWidget) -> None:
		pass

	@overload
	def __init__(self, t: TextFieldWidget, zIndex: int) -> None:
		pass

	@overload
	def getText(self) -> str:
		pass

	@overload
	def setText(self, text: str) -> "TextFieldWidgetHelper":
		pass

	@overload
	def setText(self, text: str, await: bool) -> "TextFieldWidgetHelper":
		pass

	@overload
	def setEditableColor(self, color: int) -> "TextFieldWidgetHelper":
		pass

	@overload
	def setEditable(self, edit: bool) -> "TextFieldWidgetHelper":
		pass

	@overload
	def setUneditableColor(self, color: int) -> "TextFieldWidgetHelper":
		pass

	pass



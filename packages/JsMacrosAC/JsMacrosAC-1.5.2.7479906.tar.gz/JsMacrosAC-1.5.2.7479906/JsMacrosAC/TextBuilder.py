from typing import overload
from .TextHelper import TextHelper
from .ItemStackHelper import ItemStackHelper
from .EntityHelper import EntityHelper
from .MethodWrapper import MethodWrapper


class TextBuilder:

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def append(self, text: object) -> "TextBuilder":
		pass

	@overload
	def withColor(self, color: int) -> "TextBuilder":
		pass

	@overload
	def withColor(self, r: int, g: int, b: int) -> "TextBuilder":
		pass

	@overload
	def withFormatting(self, underline: bool, bold: bool, italic: bool, strikethrough: bool, magic: bool) -> "TextBuilder":
		pass

	@overload
	def withShowTextHover(self, text: TextHelper) -> "TextBuilder":
		pass

	@overload
	def withShowItemHover(self, item: ItemStackHelper) -> "TextBuilder":
		pass

	@overload
	def withShowEntityHover(self, entity: EntityHelper) -> "TextBuilder":
		pass

	@overload
	def withCustomClickEvent(self, action: MethodWrapper) -> "TextBuilder":
		pass

	@overload
	def withClickEvent(self, action: str, value: str) -> "TextBuilder":
		pass

	@overload
	def build(self) -> TextHelper:
		pass

	pass



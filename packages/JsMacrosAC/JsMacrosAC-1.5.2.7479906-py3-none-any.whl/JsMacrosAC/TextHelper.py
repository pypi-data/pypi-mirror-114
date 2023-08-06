from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper

Text = TypeVar["net.minecraft.text.Text"]

class TextHelper(BaseHelper):

	@overload
	def __init__(self, json: str) -> None:
		pass

	@overload
	def __init__(self, t: Text) -> None:
		pass

	@overload
	def replaceFromJson(self, json: str) -> "TextHelper":
		pass

	@overload
	def replaceFromString(self, content: str) -> "TextHelper":
		pass

	@overload
	def getJson(self) -> str:
		pass

	@overload
	def getString(self) -> str:
		pass

	@overload
	def toJson(self) -> str:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



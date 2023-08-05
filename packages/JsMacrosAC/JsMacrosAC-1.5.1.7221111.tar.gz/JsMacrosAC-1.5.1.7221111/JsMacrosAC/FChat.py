from typing import overload
from .BaseLibrary import *
from .TextHelper import *
from .TextBuilder import *
from .CommandBuilder import *


class FChat(BaseLibrary):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def log(self, message: object) -> None:
		pass

	@overload
	def log(self, message: object, await: bool) -> None:
		pass

	@overload
	def say(self, message: str) -> None:
		pass

	@overload
	def say(self, message: str, await: bool) -> None:
		pass

	@overload
	def title(self, title: object, subtitle: object, fadeIn: int, remain: int, fadeOut: int) -> None:
		pass

	@overload
	def actionbar(self, text: object, tinted: bool) -> None:
		pass

	@overload
	def toast(self, title: object, desc: object) -> None:
		pass

	@overload
	def createTextHelperFromString(self, content: str) -> TextHelper:
		pass

	@overload
	def createTextHelperFromJSON(self, json: str) -> TextHelper:
		pass

	@overload
	def createTextBuilder(self) -> TextBuilder:
		pass

	@overload
	def createCommandBuilder(self, name: str) -> CommandBuilder:
		pass

	pass



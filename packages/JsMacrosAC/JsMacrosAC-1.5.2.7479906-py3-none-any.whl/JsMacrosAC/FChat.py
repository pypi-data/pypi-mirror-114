from typing import overload
from typing import TypeVar
from .BaseLibrary import BaseLibrary
from .TextHelper import TextHelper
from .TextBuilder import TextBuilder
from .CommandBuilder import CommandBuilder

Logger = TypeVar["org.apache.logging.log4j.Logger"]

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
	def getLogger(self) -> Logger:
		pass

	@overload
	def getLogger(self, name: str) -> Logger:
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



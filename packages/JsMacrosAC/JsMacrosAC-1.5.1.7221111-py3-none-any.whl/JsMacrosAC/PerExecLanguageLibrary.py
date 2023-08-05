from typing import overload
from .BaseLibrary import *
from .ContextContainer import *


class PerExecLanguageLibrary(BaseLibrary):

	@overload
	def __init__(self, context: ContextContainer, language: Class) -> None:
		pass

	pass



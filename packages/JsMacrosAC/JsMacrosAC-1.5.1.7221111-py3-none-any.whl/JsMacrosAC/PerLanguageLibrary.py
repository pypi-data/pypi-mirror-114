from typing import overload
from .BaseLibrary import *


class PerLanguageLibrary(BaseLibrary):

	@overload
	def __init__(self, language: Class) -> None:
		pass

	pass



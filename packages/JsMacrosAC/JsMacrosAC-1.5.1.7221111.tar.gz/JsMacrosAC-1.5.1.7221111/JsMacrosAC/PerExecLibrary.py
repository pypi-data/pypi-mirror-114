from typing import overload
from .BaseLibrary import *
from .ContextContainer import *


class PerExecLibrary(BaseLibrary):

	@overload
	def __init__(self, context: ContextContainer) -> None:
		pass

	pass



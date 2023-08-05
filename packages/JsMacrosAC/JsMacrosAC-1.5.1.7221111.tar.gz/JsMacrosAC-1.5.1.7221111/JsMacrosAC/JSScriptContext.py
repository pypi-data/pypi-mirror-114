from typing import overload
from .ScriptContext import *
from .BaseEvent import *


class JSScriptContext(ScriptContext):

	@overload
	def __init__(self, event: BaseEvent) -> None:
		pass

	@overload
	def isContextClosed(self) -> bool:
		pass

	@overload
	def closeContext(self) -> None:
		pass

	pass



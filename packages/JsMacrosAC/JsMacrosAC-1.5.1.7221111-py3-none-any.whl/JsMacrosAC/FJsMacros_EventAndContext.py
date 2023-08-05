from typing import overload
from .BaseEvent import *
from .ContextContainer import *


class FJsMacros_EventAndContext:
	event: BaseEvent
	context: ContextContainer

	@overload
	def __init__(self, event: BaseEvent, context: ContextContainer) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



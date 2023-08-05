from typing import overload
from .BaseListener import *
from .ScriptTrigger import *
from .Core import *
from .BaseEvent import *
from .ContextContainer import *


class KeyListener(BaseListener):

	@overload
	def __init__(self, macro: ScriptTrigger, runner: Core) -> None:
		pass

	@overload
	def trigger(self, event: BaseEvent) -> ContextContainer:
		pass

	pass



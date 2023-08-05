from typing import overload
from .IEventListener import *
from .ScriptTrigger import *
from .Core import *
from .BaseEvent import *
from .ContextContainer import *


class BaseListener(IEventListener):

	@overload
	def __init__(self, trigger: ScriptTrigger, runner: Core) -> None:
		pass

	@overload
	def getRawTrigger(self) -> ScriptTrigger:
		pass

	@overload
	def runScript(self, event: BaseEvent) -> ContextContainer:
		pass

	@overload
	def equals(self, o: object) -> bool:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



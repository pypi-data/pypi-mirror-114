from typing import overload
from typing import List
from typing import Mapping
from typing import Set
from .Core import Core
from .ScriptTrigger import ScriptTrigger
from .IEventListener import IEventListener


class BaseEventRegistry:
	oldEvents: Mapping[str, str]
	events: Set[str]

	@overload
	def __init__(self, runner: Core) -> None:
		pass

	@overload
	def clearMacros(self) -> None:
		pass

	@overload
	def addScriptTrigger(self, rawmacro: ScriptTrigger) -> None:
		pass

	@overload
	def addListener(self, event: str, listener: IEventListener) -> None:
		pass

	@overload
	def removeListener(self, event: str, listener: IEventListener) -> bool:
		pass

	@overload
	def removeListener(self, listener: IEventListener) -> bool:
		pass

	@overload
	def removeScriptTrigger(self, rawmacro: ScriptTrigger) -> bool:
		pass

	@overload
	def getListeners(self) -> Mapping[str, Set[IEventListener]]:
		pass

	@overload
	def getListeners(self, key: str) -> Set[IEventListener]:
		pass

	@overload
	def getScriptTriggers(self) -> List[ScriptTrigger]:
		pass

	@overload
	def addEvent(self, eventName: str) -> None:
		pass

	@overload
	def addEvent(self, clazz: Class) -> None:
		pass

	pass



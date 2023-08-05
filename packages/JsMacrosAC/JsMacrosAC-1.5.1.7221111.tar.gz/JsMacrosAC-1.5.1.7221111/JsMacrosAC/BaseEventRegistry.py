from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from .Core import *
from .ScriptTrigger import *
from .IEventListener import *

Set = TypeVar["java.util.Set_xyz.wagyourtail.jsmacros.core.event.IEventListener_"]
List = TypeVar["java.util.List_xyz.wagyourtail.jsmacros.core.config.ScriptTrigger_"]
Map = TypeVar["java.util.Map_java.lang.String,java.util.Set_xyz.wagyourtail.jsmacros.core.event.IEventListener__"]

class BaseEventRegistry:
	oldEvents: Mapping[str, str]
	events: List[str]

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
	def getListeners(self) -> Mapping[str, List[IEventListener]]:
		pass

	@overload
	def getListeners(self, key: str) -> List[IEventListener]:
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



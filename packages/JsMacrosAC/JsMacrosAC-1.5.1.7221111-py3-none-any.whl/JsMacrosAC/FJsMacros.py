from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from .BaseLibrary import *
from .BaseProfile import *
from .ConfigManager import *
from .ScriptTrigger import *
from .ScriptContext import *
from .ContextContainer import *
from .MethodWrapper import *
from .IEventListener import *
from .FJsMacros_EventAndContext import *
from .EventCustom import *

Set = TypeVar["java.util.Set_java.lang.Object_"]
List = TypeVar["java.util.List_xyz.wagyourtail.jsmacros.core.event.IEventListener_"]
Map = TypeVar["java.util.Map_xyz.wagyourtail.jsmacros.core.config.ScriptTrigger,java.util.Set_java.lang.Object__"]

class FJsMacros(BaseLibrary):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def getProfile(self) -> BaseProfile:
		pass

	@overload
	def getConfig(self) -> ConfigManager:
		pass

	@overload
	def getRunningThreads(self) -> Mapping[ScriptTrigger, List[object]]:
		pass

	@overload
	def getOpenContexts(self) -> List[ScriptContext]:
		pass

	@overload
	def runScript(self, file: str) -> ContextContainer:
		pass

	@overload
	def runScript(self, file: str, callback: MethodWrapper) -> ContextContainer:
		pass

	@overload
	def runScript(self, language: str, script: str) -> ContextContainer:
		pass

	@overload
	def runScript(self, language: str, script: str, callback: MethodWrapper) -> ContextContainer:
		pass

	@overload
	def open(self, path: str) -> None:
		pass

	@overload
	def on(self, event: str, callback: MethodWrapper) -> IEventListener:
		pass

	@overload
	def once(self, event: str, callback: MethodWrapper) -> IEventListener:
		pass

	@overload
	def off(self, listener: IEventListener) -> bool:
		pass

	@overload
	def off(self, event: str, listener: IEventListener) -> bool:
		pass

	@overload
	def waitForEvent(self, event: str) -> FJsMacros_EventAndContext:
		pass

	@overload
	def waitForEvent(self, event: str, filter: MethodWrapper) -> FJsMacros_EventAndContext:
		pass

	@overload
	def waitForEvent(self, event: str, filter: MethodWrapper, runBeforeWaiting: MethodWrapper) -> FJsMacros_EventAndContext:
		pass

	@overload
	def listeners(self, event: str) -> List[IEventListener]:
		pass

	@overload
	def createCustomEvent(self, eventName: str) -> EventCustom:
		pass

	pass



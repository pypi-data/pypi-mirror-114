from typing import overload
from typing import List
from .PerExecLibrary import PerExecLibrary
from .BaseScriptContext import BaseScriptContext
from .BaseProfile import BaseProfile
from .ConfigManager import ConfigManager
from .EventContainer import EventContainer
from .MethodWrapper import MethodWrapper
from .IEventListener import IEventListener
from .FJsMacros_EventAndContext import FJsMacros_EventAndContext
from .EventCustom import EventCustom


class FJsMacros(PerExecLibrary):

	@overload
	def __init__(self, context: BaseScriptContext) -> None:
		pass

	@overload
	def getProfile(self) -> BaseProfile:
		pass

	@overload
	def getConfig(self) -> ConfigManager:
		pass

	@overload
	def getOpenContexts(self) -> List[BaseScriptContext]:
		pass

	@overload
	def runScript(self, file: str) -> EventContainer:
		pass

	@overload
	def runScript(self, file: str, callback: MethodWrapper) -> EventContainer:
		pass

	@overload
	def runScript(self, language: str, script: str) -> EventContainer:
		pass

	@overload
	def runScript(self, language: str, script: str, callback: MethodWrapper) -> EventContainer:
		pass

	@overload
	def runScript(self, language: str, script: str, file: str, callback: MethodWrapper) -> EventContainer:
		pass

	@overload
	def open(self, path: str) -> None:
		pass

	@overload
	def openUrl(self, url: str) -> None:
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



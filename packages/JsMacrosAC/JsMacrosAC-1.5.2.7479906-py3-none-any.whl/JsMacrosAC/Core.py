from typing import overload
from typing import List
from typing import TypeVar
from typing import Set
from typing import Generic
from .LibraryRegistry import LibraryRegistry
from .BaseEventRegistry import BaseEventRegistry
from .ConfigManager import ConfigManager
from .BaseLanguage import BaseLanguage
from .EventContainer import EventContainer
from .BaseScriptContext import BaseScriptContext
from .ScriptTrigger import ScriptTrigger
from .BaseEvent import BaseEvent
from .BaseWrappedException import BaseWrappedException

Function = TypeVar["java.util.function.Function_xyz.wagyourtail.jsmacros.core.Core_V,R_,V_"]
T = TypeVar("T")
Consumer = TypeVar["java.util.function.Consumer_java.lang.Throwable_"]
U = TypeVar("U")
Runnable = TypeVar["java.lang.Runnable"]
Throwable = TypeVar["java.lang.Throwable"]
Logger = TypeVar["org.apache.logging.log4j.Logger"]
File = TypeVar["java.io.File"]

class Core(Generic[T, U]):
	instance: "Core"
	libraryRegistry: LibraryRegistry
	eventRegistry: BaseEventRegistry
	profile: T
	config: ConfigManager
	languages: List[BaseLanguage]
	defaultLang: BaseLanguage

	@overload
	def addContext(self, container: EventContainer) -> None:
		pass

	@overload
	def getContexts(self) -> Set[BaseScriptContext]:
		pass

	@overload
	def createInstance(self, eventRegistryFunction: Function, profileFunction: Function, configFolder: File, macroFolder: File, logger: Logger) -> "Core":
		pass

	@overload
	def addLanguage(self, l: BaseLanguage) -> None:
		pass

	@overload
	def exec(self, macro: ScriptTrigger, event: BaseEvent) -> EventContainer:
		pass

	@overload
	def exec(self, macro: ScriptTrigger, event: BaseEvent, then: Runnable, catcher: Consumer) -> EventContainer:
		pass

	@overload
	def exec(self, lang: str, script: str, fakeFile: File, then: Runnable, catcher: Consumer) -> EventContainer:
		pass

	@overload
	def wrapException(self, ex: Throwable) -> BaseWrappedException:
		pass

	pass



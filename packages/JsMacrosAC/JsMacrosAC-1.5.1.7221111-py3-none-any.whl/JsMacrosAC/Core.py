from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from .Core import *
from .BaseEventRegistry import *
from .BaseProfile import *
from .ConfigManager import *
from .LibraryRegistry import *
from .ScriptContext import *
from .ContextContainer import *
from .BaseLanguage import *
from .ScriptTrigger import *
from .BaseEvent import *
from .BaseWrappedException import *

Function = TypeVar["java.util.function.Function_xyz.wagyourtail.jsmacros.core.Core,xyz.wagyourtail.jsmacros.core.config.BaseProfile_"]
Consumer = TypeVar["java.util.function.Consumer_java.lang.Throwable_"]
Runnable = TypeVar["java.lang.Runnable"]
Throwable = TypeVar["java.lang.Throwable"]
List = TypeVar["java.util.List_xyz.wagyourtail.jsmacros.core.language.BaseLanguage___"]
Logger = TypeVar["org.apache.logging.log4j.Logger"]
Map = TypeVar["java.util.Map_java.lang.Thread,xyz.wagyourtail.jsmacros.core.language.ContextContainer___"]
File = TypeVar["java.io.File"]
Thread = TypeVar["java.lang.Thread"]

class Core:
	instance: "Core"
	eventRegistry: BaseEventRegistry
	profile: BaseProfile
	config: ConfigManager
	libraryRegistry: LibraryRegistry
	contexts: Mapping[ScriptContext, str]
	threadContext: Mapping[Thread, ScriptContext]
	eventContexts: Mapping[Thread, ContextContainer]
	languages: List[BaseLanguage]
	defaultLang: BaseLanguage

	@overload
	def createInstance(self, eventRegistryFunction: Function, profileFunction: Function, configFolder: File, macroFolder: File, logger: Logger) -> "Core":
		pass

	@overload
	def addLanguage(self, l: BaseLanguage) -> None:
		pass

	@overload
	def sortLanguages(self) -> None:
		pass

	@overload
	def exec(self, macro: ScriptTrigger, event: BaseEvent) -> ContextContainer:
		pass

	@overload
	def exec(self, macro: ScriptTrigger, event: BaseEvent, then: Runnable, catcher: Consumer) -> ContextContainer:
		pass

	@overload
	def wrapException(self, ex: Throwable) -> BaseWrappedException:
		pass

	pass



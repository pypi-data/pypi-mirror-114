from typing import overload
from typing import TypeVar
from typing import Mapping
from .Core import *
from .ScriptTrigger import *
from .BaseEvent import *
from .ContextContainer import *
from .BaseLibrary import *
from .BaseWrappedException import *
from .ScriptContext import *

Consumer = TypeVar["java.util.function.Consumer_java.lang.Throwable_"]
Runnable = TypeVar["java.lang.Runnable"]
Throwable = TypeVar["java.lang.Throwable"]
Map = TypeVar["java.util.Map_java.lang.String,xyz.wagyourtail.jsmacros.core.library.BaseLibrary_"]

class BaseLanguage:
	extension: str

	@overload
	def __init__(self, extension: str, runner: Core) -> None:
		pass

	@overload
	def trigger(self, macro: ScriptTrigger, event: BaseEvent, then: Runnable, catcher: Consumer) -> ContextContainer:
		pass

	@overload
	def trigger(self, script: str, then: Runnable, catcher: Consumer) -> ContextContainer:
		pass

	@overload
	def retrieveLibs(self, context: ContextContainer) -> Mapping[str, BaseLibrary]:
		pass

	@overload
	def retrieveOnceLibs(self) -> Mapping[str, BaseLibrary]:
		pass

	@overload
	def retrievePerExecLibs(self, context: ContextContainer) -> Mapping[str, BaseLibrary]:
		pass

	@overload
	def wrapException(self, ex: Throwable) -> BaseWrappedException:
		pass

	@overload
	def createContext(self, event: BaseEvent) -> ScriptContext:
		pass

	@overload
	def extension(self) -> str:
		pass

	pass



from typing import overload
from typing import TypeVar
from .BaseLanguage import *
from .Core import *
from .BaseWrappedException import *
from .BaseEvent import *
from .JSScriptContext import *

Throwable = TypeVar["java.lang.Throwable"]

class JavascriptLanguageDefinition(BaseLanguage):

	@overload
	def __init__(self, extension: str, runner: Core) -> None:
		pass

	@overload
	def wrapException(self, ex: Throwable) -> BaseWrappedException:
		pass

	@overload
	def createContext(self, event: BaseEvent) -> JSScriptContext:
		pass

	pass



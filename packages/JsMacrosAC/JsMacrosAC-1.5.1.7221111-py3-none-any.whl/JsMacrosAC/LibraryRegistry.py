from typing import overload
from typing import TypeVar
from typing import Mapping
from .Library import *
from .BaseLibrary import *
from .PerLanguageLibrary import *
from .BaseLanguage import *
from .ContextContainer import *

Map = TypeVar["java.util.Map_java.lang.String,xyz.wagyourtail.jsmacros.core.library.BaseLibrary_"]

class LibraryRegistry:
	libraries: Mapping[Library, BaseLibrary]
	perExec: Mapping[Library, Class]
	perLanguage: Mapping[Class, Mapping[Library, PerLanguageLibrary]]
	perExecLanguage: Mapping[Class, Mapping[Library, Class]]

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def getLibraries(self, language: BaseLanguage, context: ContextContainer) -> Mapping[str, BaseLibrary]:
		pass

	@overload
	def getOnceLibraries(self, language: BaseLanguage) -> Mapping[str, BaseLibrary]:
		pass

	@overload
	def getPerExecLibraries(self, language: BaseLanguage, context: ContextContainer) -> Mapping[str, BaseLibrary]:
		pass

	@overload
	def addLibrary(self, clazz: Class) -> None:
		pass

	pass



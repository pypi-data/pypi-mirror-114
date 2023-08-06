from typing import overload
from typing import List
from typing import TypeVar
from .PerExecLibrary import PerExecLibrary
from .BaseScriptContext import BaseScriptContext
from .Mappings import Mappings

Field = TypeVar["java.lang.reflect.Field"]
T = TypeVar("T")
Method = TypeVar["java.lang.reflect.Method"]

class FReflection(PerExecLibrary):

	@overload
	def __init__(self, context: BaseScriptContext) -> None:
		pass

	@overload
	def getClass(self, name: str) -> Class:
		pass

	@overload
	def getClass(self, name: str, name2: str) -> Class:
		pass

	@overload
	def getDeclaredMethod(self, c: Class, name: str, parameterTypes: List[Class]) -> Method:
		pass

	@overload
	def getDeclaredMethod(self, c: Class, name: str, name2: str, parameterTypes: List[Class]) -> Method:
		pass

	@overload
	def getDeclaredField(self, c: Class, name: str) -> Field:
		pass

	@overload
	def getDeclaredField(self, c: Class, name: str, name2: str) -> Field:
		pass

	@overload
	def invokeMethod(self, m: Method, c: object, objects: List[object]) -> object:
		pass

	@overload
	def newInstance(self, c: Class, objects: List[object]) -> T:
		pass

	@overload
	def loadJarFile(self, file: str) -> bool:
		pass

	@overload
	def loadCurrentMappingHelper(self) -> Mappings:
		pass

	@overload
	def getClassName(self, o: object) -> str:
		pass

	@overload
	def loadMappingHelper(self, urlorfile: str) -> Mappings:
		pass

	pass



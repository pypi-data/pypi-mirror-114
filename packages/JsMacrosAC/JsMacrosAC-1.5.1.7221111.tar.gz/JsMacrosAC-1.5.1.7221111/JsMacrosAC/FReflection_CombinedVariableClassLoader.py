from typing import overload
from typing import TypeVar

File = TypeVar["java.io.File"]

class FReflection_CombinedVariableClassLoader(ClassLoader):

	@overload
	def __init__(self, parent: ClassLoader) -> None:
		pass

	@overload
	def addClassLoader(self, jarPath: File, loader: ClassLoader) -> bool:
		pass

	@overload
	def hasJar(self, path: File) -> bool:
		pass

	pass



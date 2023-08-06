from typing import overload
from typing import List
from typing import TypeVar

File = TypeVar["java.io.File"]

class FileHandler:

	@overload
	def __init__(self, path: str) -> None:
		pass

	@overload
	def __init__(self, path: File) -> None:
		pass

	@overload
	def write(self, s: str) -> "FileHandler":
		pass

	@overload
	def write(self, b: List[float]) -> "FileHandler":
		pass

	@overload
	def read(self) -> str:
		pass

	@overload
	def readBytes(self) -> List[float]:
		pass

	@overload
	def append(self, s: str) -> "FileHandler":
		pass

	@overload
	def append(self, b: List[float]) -> "FileHandler":
		pass

	@overload
	def getFile(self) -> File:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



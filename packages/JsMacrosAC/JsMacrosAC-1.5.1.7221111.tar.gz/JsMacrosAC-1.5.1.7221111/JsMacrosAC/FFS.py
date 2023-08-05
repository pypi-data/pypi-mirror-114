from typing import overload
from typing import List
from .BaseLibrary import *
from .FileHandler import *


class FFS(BaseLibrary):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def list(self, path: str) -> List[str]:
		pass

	@overload
	def exists(self, path: str) -> bool:
		pass

	@overload
	def isDir(self, path: str) -> bool:
		pass

	@overload
	def getName(self, path: str) -> str:
		pass

	@overload
	def makeDir(self, path: str) -> bool:
		pass

	@overload
	def move(self, from: str, to: str) -> None:
		pass

	@overload
	def copy(self, from: str, to: str) -> None:
		pass

	@overload
	def unlink(self, path: str) -> bool:
		pass

	@overload
	def combine(self, patha: str, pathb: str) -> str:
		pass

	@overload
	def getDir(self, path: str) -> str:
		pass

	@overload
	def open(self, path: str) -> FileHandler:
		pass

	pass



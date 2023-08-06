from typing import overload
from typing import Mapping
from .BaseLibrary import BaseLibrary


class FGlobalVars(BaseLibrary):
	globalRaw: Mapping[str, object]

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def putInt(self, name: str, i: int) -> int:
		pass

	@overload
	def putString(self, name: str, str: str) -> str:
		pass

	@overload
	def putDouble(self, name: str, d: float) -> float:
		pass

	@overload
	def putBoolean(self, name: str, b: bool) -> bool:
		pass

	@overload
	def putObject(self, name: str, o: object) -> object:
		pass

	@overload
	def getType(self, name: str) -> str:
		pass

	@overload
	def getInt(self, name: str) -> int:
		pass

	@overload
	def getString(self, name: str) -> str:
		pass

	@overload
	def getDouble(self, name: str) -> float:
		pass

	@overload
	def getBoolean(self, name: str) -> bool:
		pass

	@overload
	def getObject(self, name: str) -> object:
		pass

	@overload
	def remove(self, key: str) -> None:
		pass

	@overload
	def getRaw(self) -> Mapping[str, object]:
		pass

	pass



from typing import overload
from typing import List
from typing import TypeVar
from typing import Any

Set = TypeVar["java.util.Set_java.lang.String_"]
T = TypeVar["T"]
Collection = TypeVar["java.util.Collection_java.lang.String_"]

class StringHashTrie:

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def size(self) -> int:
		pass

	@overload
	def isEmpty(self) -> bool:
		pass

	@overload
	def contains(self, o: object) -> bool:
		pass

	@overload
	def iterator(self) -> iter:
		pass

	@overload
	def toArray(self) -> List[str]:
		pass

	@overload
	def toArray(self, a: List[T]) -> List[T]:
		pass

	@overload
	def add(self, s: str) -> bool:
		pass

	@overload
	def remove(self, o: object) -> bool:
		pass

	@overload
	def containsAll(self, c: List[Any]) -> bool:
		pass

	@overload
	def containsAll(self, o: List[str]) -> bool:
		pass

	@overload
	def addAll(self, c: List[Any]) -> bool:
		pass

	@overload
	def addAll(self, o: List[str]) -> bool:
		pass

	@overload
	def removeAll(self, c: List[Any]) -> bool:
		pass

	@overload
	def removeAll(self, o: List[str]) -> bool:
		pass

	@overload
	def retainAll(self, c: List[Any]) -> bool:
		pass

	@overload
	def retainAll(self, o: List[str]) -> bool:
		pass

	@overload
	def clear(self) -> None:
		pass

	@overload
	def getAllWithPrefix(self, prefix: str) -> List[str]:
		pass

	@overload
	def getAllWithPrefixCaseInsensitive(self, prefix: str) -> List[str]:
		pass

	@overload
	def getAll(self) -> List[str]:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



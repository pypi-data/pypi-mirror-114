from typing import overload
from typing import List
from typing import TypeVar

Set = TypeVar["java.util.Set_java.lang.String_"]

class AutoCompleteSuggestor:

	@overload
	def __init__(self, language: str) -> None:
		pass

	@overload
	def getSuggestions(self, start: str) -> List[str]:
		pass

	pass



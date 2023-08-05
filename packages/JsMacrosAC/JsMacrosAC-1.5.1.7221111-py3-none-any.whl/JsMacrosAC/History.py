from typing import overload
from typing import TypeVar
from .SelectCursor import *

Consumer = TypeVar["java.util.function.Consumer_java.lang.String_"]

class History:
	onChange: Consumer
	current: str

	@overload
	def __init__(self, start: str, cursor: SelectCursor) -> None:
		pass

	@overload
	def addChar(self, position: int, content: str) -> bool:
		pass

	@overload
	def add(self, position: int, content: str) -> bool:
		pass

	@overload
	def deletePos(self, position: int, length: int) -> bool:
		pass

	@overload
	def bkspacePos(self, position: int, length: int) -> bool:
		pass

	@overload
	def shiftLine(self, startLine: int, lines: int, shiftDown: bool) -> bool:
		pass

	@overload
	def replace(self, position: int, length: int, content: str) -> None:
		pass

	@overload
	def tabLines(self, startLine: int, lineCount: int, reverse: bool) -> None:
		pass

	@overload
	def undo(self) -> int:
		pass

	@overload
	def redo(self) -> int:
		pass

	pass



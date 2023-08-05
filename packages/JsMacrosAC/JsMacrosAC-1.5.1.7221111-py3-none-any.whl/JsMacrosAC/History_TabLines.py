from typing import overload
from .History_HistoryStep import *
from .SelectCursor import *


class History_TabLines(History_HistoryStep):

	@overload
	def __init__(self, startLine: int, lineCount: int, reversed: bool, cursor: SelectCursor) -> None:
		pass

	pass



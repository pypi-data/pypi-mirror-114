from typing import overload
from .BaseLibrary import BaseLibrary


class FTime(BaseLibrary):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def time(self) -> float:
		pass

	@overload
	def sleep(self, millis: float) -> None:
		pass

	pass



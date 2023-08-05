from typing import overload
from typing import TypeVar

T = TypeVar["T"]

class BaseHelper:

	@overload
	def __init__(self, base: T) -> None:
		pass

	@overload
	def getRaw(self) -> T:
		pass

	pass



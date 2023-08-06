from typing import overload
from typing import TypeVar
from .MethodWrapper import MethodWrapper

T = TypeVar("T")

class IFWrapper:

	@overload
	def methodToJava(self, c: T) -> MethodWrapper:
		pass

	@overload
	def methodToJavaAsync(self, c: T) -> MethodWrapper:
		pass

	@overload
	def stop(self) -> None:
		pass

	pass



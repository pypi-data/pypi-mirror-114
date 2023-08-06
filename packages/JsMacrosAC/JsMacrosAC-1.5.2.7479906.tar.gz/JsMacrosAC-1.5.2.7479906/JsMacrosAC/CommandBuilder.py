from typing import overload
from .MethodWrapper import MethodWrapper


class CommandBuilder:

	@overload
	def __init__(self, name: str) -> None:
		pass

	@overload
	def literalArg(self, name: str) -> "CommandBuilder":
		pass

	@overload
	def angleArg(self, name: str) -> "CommandBuilder":
		pass

	@overload
	def blockArg(self, name: str) -> "CommandBuilder":
		pass

	@overload
	def booleanArg(self, name: str) -> "CommandBuilder":
		pass

	@overload
	def colorArg(self, name: str) -> "CommandBuilder":
		pass

	@overload
	def doubleArg(self, name: str) -> "CommandBuilder":
		pass

	@overload
	def doubleArg(self, name: str, min: float, max: float) -> "CommandBuilder":
		pass

	@overload
	def floatRangeArg(self, name: str) -> "CommandBuilder":
		pass

	@overload
	def longArg(self, name: str) -> "CommandBuilder":
		pass

	@overload
	def longArg(self, name: str, min: float, max: float) -> "CommandBuilder":
		pass

	@overload
	def identifierArg(self, name: str) -> "CommandBuilder":
		pass

	@overload
	def intArg(self, name: str) -> "CommandBuilder":
		pass

	@overload
	def intArg(self, name: str, min: int, max: int) -> "CommandBuilder":
		pass

	@overload
	def intRangeArg(self, name: str) -> "CommandBuilder":
		pass

	@overload
	def itemArg(self, name: str) -> "CommandBuilder":
		pass

	@overload
	def nbtArg(self, name: str) -> "CommandBuilder":
		pass

	@overload
	def greedyStringArg(self, name: str) -> "CommandBuilder":
		pass

	@overload
	def quotedStringArg(self, name: str) -> "CommandBuilder":
		pass

	@overload
	def wordArg(self, name: str) -> "CommandBuilder":
		pass

	@overload
	def textArgType(self, name: str) -> "CommandBuilder":
		pass

	@overload
	def uuidArgType(self, name: str) -> "CommandBuilder":
		pass

	@overload
	def regexArgType(self, name: str, regex: str, flags: str) -> "CommandBuilder":
		pass

	@overload
	def executes(self, callback: MethodWrapper) -> "CommandBuilder":
		pass

	@overload
	def or(self) -> "CommandBuilder":
		pass

	@overload
	def otherwise(self) -> "CommandBuilder":
		pass

	@overload
	def or(self, argumentLevel: int) -> "CommandBuilder":
		pass

	@overload
	def otherwise(self, argLevel: int) -> "CommandBuilder":
		pass

	@overload
	def register(self) -> None:
		pass

	pass



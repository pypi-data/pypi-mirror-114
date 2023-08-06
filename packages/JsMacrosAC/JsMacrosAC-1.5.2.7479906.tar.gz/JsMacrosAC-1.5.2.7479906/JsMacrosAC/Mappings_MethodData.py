from typing import overload


class Mappings_MethodData:
	name: str
	sig: str

	@overload
	def __init__(self, name: str, sig: str) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



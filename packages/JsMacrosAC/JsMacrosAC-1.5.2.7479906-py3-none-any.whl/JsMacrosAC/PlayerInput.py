from typing import overload
from typing import List
from typing import TypeVar

Input = TypeVar["net.minecraft.client.input.Input"]

class PlayerInput:
	movementForward: float
	movementSideways: float
	yaw: float
	pitch: float
	jumping: bool
	sneaking: bool
	sprinting: bool

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def __init__(self, movementForward: float, movementSideways: float, yaw: float) -> None:
		pass

	@overload
	def __init__(self, movementForward: float, yaw: float, jumping: bool, sprinting: bool) -> None:
		pass

	@overload
	def __init__(self, input: Input, yaw: float, pitch: float, sprinting: bool) -> None:
		pass

	@overload
	def __init__(self, movementForward: float, movementSideways: float, yaw: float, pitch: float, jumping: bool, sneaking: bool, sprinting: bool) -> None:
		pass

	@overload
	def __init__(self, movementForward: float, movementSideways: float, yaw: float, pitch: float, jumping: bool, sneaking: bool, sprinting: bool) -> None:
		pass

	@overload
	def __init__(self, input: "PlayerInput") -> None:
		pass

	@overload
	def fromCsv(self, csv: str) -> List["PlayerInput"]:
		pass

	@overload
	def fromJson(self, json: str) -> "PlayerInput":
		pass

	@overload
	def toString(self, varNames: bool) -> str:
		pass

	@overload
	def toString(self) -> str:
		pass

	@overload
	def clone(self) -> "PlayerInput":
		pass

	pass



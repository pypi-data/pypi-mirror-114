from typing import overload
from typing import TypeVar
from typing import Generic
from .PlayerEntityHelper import PlayerEntityHelper
from .EntityHelper import EntityHelper

T = TypeVar("T")

class ClientPlayerEntityHelper(Generic[T], PlayerEntityHelper):

	@overload
	def __init__(self, e: T) -> None:
		pass

	@overload
	def lookAt(self, yaw: float, pitch: float) -> "ClientPlayerEntityHelper":
		pass

	@overload
	def lookAt(self, x: float, y: float, z: float) -> "ClientPlayerEntityHelper":
		pass

	@overload
	def attack(self, entity: EntityHelper) -> None:
		pass

	@overload
	def attack(self, x: int, y: int, z: int, direction: int) -> None:
		pass

	@overload
	def interact(self, entity: EntityHelper, offHand: bool) -> None:
		pass

	@overload
	def interact(self, offHand: bool) -> None:
		pass

	@overload
	def interact(self, x: int, y: int, z: int, direction: int, offHand: bool) -> None:
		pass

	@overload
	def interact(self) -> None:
		pass

	@overload
	def attack(self) -> None:
		pass

	@overload
	def getFoodLevel(self) -> int:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



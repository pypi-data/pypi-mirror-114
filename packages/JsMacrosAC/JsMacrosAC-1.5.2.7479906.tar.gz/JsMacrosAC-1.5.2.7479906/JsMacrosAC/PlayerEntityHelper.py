from typing import overload
from typing import TypeVar
from typing import Generic
from .LivingEntityHelper import LivingEntityHelper
from .PlayerAbilitiesHelper import PlayerAbilitiesHelper
from .ItemStackHelper import ItemStackHelper

T = TypeVar("T")

class PlayerEntityHelper(Generic[T], LivingEntityHelper):

	@overload
	def __init__(self, e: T) -> None:
		pass

	@overload
	def getAbilities(self) -> PlayerAbilitiesHelper:
		pass

	@overload
	def getMainHand(self) -> ItemStackHelper:
		pass

	@overload
	def getOffHand(self) -> ItemStackHelper:
		pass

	@overload
	def getHeadArmor(self) -> ItemStackHelper:
		pass

	@overload
	def getChestArmor(self) -> ItemStackHelper:
		pass

	@overload
	def getLegArmor(self) -> ItemStackHelper:
		pass

	@overload
	def getFootArmor(self) -> ItemStackHelper:
		pass

	@overload
	def getXP(self) -> int:
		pass

	@overload
	def isSleeping(self) -> bool:
		pass

	@overload
	def isSleepingLongEnough(self) -> bool:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



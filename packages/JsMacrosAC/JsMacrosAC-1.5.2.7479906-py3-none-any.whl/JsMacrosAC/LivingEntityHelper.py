from typing import overload
from typing import List
from typing import TypeVar
from typing import Generic
from .EntityHelper import EntityHelper
from .StatusEffectHelper import StatusEffectHelper
from .ItemStackHelper import ItemStackHelper

T = TypeVar("T")

class LivingEntityHelper(Generic[T], EntityHelper):

	@overload
	def __init__(self, e: T) -> None:
		pass

	@overload
	def getStatusEffects(self) -> List[StatusEffectHelper]:
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
	def getHealth(self) -> float:
		pass

	@overload
	def isSleeping(self) -> bool:
		pass

	@overload
	def isFallFlying(self) -> bool:
		pass

	pass



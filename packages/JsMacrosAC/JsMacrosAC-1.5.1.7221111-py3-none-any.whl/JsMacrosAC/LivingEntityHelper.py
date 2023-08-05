from typing import overload
from typing import List
from typing import TypeVar
from .EntityHelper import *
from .StatusEffectHelper import *
from .ItemStackHelper import *

T = TypeVar["T"]
List = TypeVar["java.util.List_xyz.wagyourtail.jsmacros.client.api.helpers.StatusEffectHelper_"]

class LivingEntityHelper(EntityHelper):

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



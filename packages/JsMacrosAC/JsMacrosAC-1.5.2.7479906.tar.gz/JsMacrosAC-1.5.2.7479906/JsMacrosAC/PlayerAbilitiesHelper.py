from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper

PlayerAbilities = TypeVar["net.minecraft.entity.player.PlayerAbilities"]

class PlayerAbilitiesHelper(BaseHelper):

	@overload
	def __init__(self, a: PlayerAbilities) -> None:
		pass

	@overload
	def getInvulnerable(self) -> bool:
		pass

	@overload
	def getFlying(self) -> bool:
		pass

	@overload
	def getAllowFlying(self) -> bool:
		pass

	@overload
	def getCreativeMode(self) -> bool:
		pass

	@overload
	def setFlying(self, b: bool) -> "PlayerAbilitiesHelper":
		pass

	@overload
	def setAllowFlying(self, b: bool) -> "PlayerAbilitiesHelper":
		pass

	@overload
	def getFlySpeed(self) -> float:
		pass

	@overload
	def setFlySpeed(self, flySpeed: float) -> "PlayerAbilitiesHelper":
		pass

	pass



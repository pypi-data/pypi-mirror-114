from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper

StatusEffectInstance = TypeVar["net.minecraft.entity.effect.StatusEffectInstance"]

class StatusEffectHelper(BaseHelper):

	@overload
	def __init__(self, s: StatusEffectInstance) -> None:
		pass

	@overload
	def getId(self) -> str:
		pass

	@overload
	def getStrength(self) -> int:
		pass

	@overload
	def getTime(self) -> int:
		pass

	pass



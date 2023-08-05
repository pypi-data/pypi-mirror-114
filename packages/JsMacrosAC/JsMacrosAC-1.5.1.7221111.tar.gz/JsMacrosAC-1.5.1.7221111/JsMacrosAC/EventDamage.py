from typing import overload
from typing import TypeVar
from .BaseEvent import *
from .EntityHelper import *

DamageSource = TypeVar["net.minecraft.entity.damage.DamageSource"]

class EventDamage(BaseEvent):
	attacker: EntityHelper
	source: str
	health: float
	change: float

	@overload
	def __init__(self, source: DamageSource, health: float, change: float) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



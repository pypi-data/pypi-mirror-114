from typing import overload
from typing import TypeVar
from .BaseEvent import *
from .EntityHelper import *

Entity = TypeVar["net.minecraft.entity.Entity"]

class EventEntityDamaged(BaseEvent):
	entity: EntityHelper
	damage: float

	@overload
	def __init__(self, e: Entity, amount: float) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



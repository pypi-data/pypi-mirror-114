from typing import overload
from typing import TypeVar
from .BaseEvent import BaseEvent
from .EntityHelper import EntityHelper

Entity = TypeVar["net.minecraft.entity.Entity"]

class EventRiding(BaseEvent):
	state: bool
	entity: EntityHelper

	@overload
	def __init__(self, state: bool, entity: Entity) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



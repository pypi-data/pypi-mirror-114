from typing import overload
from typing import TypeVar
from .BaseEvent import *
from .EntityHelper import *

Entity = TypeVar["net.minecraft.entity.Entity"]

class EventEntityLoad(BaseEvent):
	entity: EntityHelper

	@overload
	def __init__(self, e: Entity) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



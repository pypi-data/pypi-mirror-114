from typing import overload
from typing import TypeVar
from .BaseEvent import *
from .ItemStackHelper import *

ItemStack = TypeVar["net.minecraft.item.ItemStack"]

class EventItemDamage(BaseEvent):
	item: ItemStackHelper
	damage: int

	@overload
	def __init__(self, stack: ItemStack, damage: int) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



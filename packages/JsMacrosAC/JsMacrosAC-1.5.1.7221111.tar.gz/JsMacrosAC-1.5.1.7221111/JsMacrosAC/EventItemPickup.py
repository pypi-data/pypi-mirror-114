from typing import overload
from typing import TypeVar
from .BaseEvent import *
from .ItemStackHelper import *

ItemStack = TypeVar["net.minecraft.item.ItemStack"]

class EventItemPickup(BaseEvent):
	item: ItemStackHelper

	@overload
	def __init__(self, item: ItemStack) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



from typing import overload
from typing import TypeVar

ItemStack = TypeVar["net.minecraft.item.ItemStack"]

class TickBasedEvents:

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def areNotEqual(self, a: ItemStack, b: ItemStack) -> bool:
		pass

	@overload
	def areTagsEqualIgnoreDamage(self, a: ItemStack, b: ItemStack) -> bool:
		pass

	@overload
	def areEqualIgnoreDamage(self, a: ItemStack, b: ItemStack) -> bool:
		pass

	@overload
	def init(self) -> None:
		pass

	pass



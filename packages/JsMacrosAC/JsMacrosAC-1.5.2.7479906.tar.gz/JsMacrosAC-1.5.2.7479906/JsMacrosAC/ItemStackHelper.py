from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper
from .NBTElementHelper import NBTElementHelper

ItemStack = TypeVar["net.minecraft.item.ItemStack"]

class ItemStackHelper(BaseHelper):

	@overload
	def __init__(self, i: ItemStack) -> None:
		pass

	@overload
	def setDamage(self, damage: int) -> "ItemStackHelper":
		pass

	@overload
	def isDamageable(self) -> bool:
		pass

	@overload
	def isEnchantable(self) -> bool:
		pass

	@overload
	def getDamage(self) -> int:
		pass

	@overload
	def getMaxDamage(self) -> int:
		pass

	@overload
	def getDefaultName(self) -> str:
		pass

	@overload
	def getName(self) -> str:
		pass

	@overload
	def getCount(self) -> int:
		pass

	@overload
	def getMaxCount(self) -> int:
		pass

	@overload
	def getNBT(self) -> NBTElementHelper:
		pass

	@overload
	def getCreativeTab(self) -> str:
		pass

	@overload
	def getItemID(self) -> str:
		pass

	@overload
	def isEmpty(self) -> bool:
		pass

	@overload
	def toString(self) -> str:
		pass

	@overload
	def equals(self, ish: "ItemStackHelper") -> bool:
		pass

	@overload
	def equals(self, is: ItemStack) -> bool:
		pass

	@overload
	def isItemEqual(self, ish: "ItemStackHelper") -> bool:
		pass

	@overload
	def isItemEqual(self, is: ItemStack) -> bool:
		pass

	@overload
	def isItemEqualIgnoreDamage(self, ish: "ItemStackHelper") -> bool:
		pass

	@overload
	def isItemEqualIgnoreDamage(self, is: ItemStack) -> bool:
		pass

	@overload
	def isNBTEqual(self, ish: "ItemStackHelper") -> bool:
		pass

	@overload
	def isNBTEqual(self, is: ItemStack) -> bool:
		pass

	@overload
	def copy(self) -> "ItemStackHelper":
		pass

	pass



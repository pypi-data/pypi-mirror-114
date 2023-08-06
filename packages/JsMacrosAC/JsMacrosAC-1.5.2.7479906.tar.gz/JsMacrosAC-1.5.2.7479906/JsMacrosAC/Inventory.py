from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from typing import Generic
from .ItemStackHelper import ItemStackHelper
from .RecipeHelper import RecipeHelper

T = TypeVar("T")

class Inventory(Generic[T]):

	@overload
	def create(self) -> "Inventory":
		pass

	@overload
	def click(self, slot: int) -> "Inventory":
		pass

	@overload
	def click(self, slot: int, mousebutton: int) -> "Inventory":
		pass

	@overload
	def dragClick(self, slots: List[int], mousebutton: int) -> "Inventory":
		pass

	@overload
	def dropSlot(self, slot: int) -> "Inventory":
		pass

	@overload
	def getSelectedHotbarSlotIndex(self) -> int:
		pass

	@overload
	def setSelectedHotbarSlotIndex(self, index: int) -> None:
		pass

	@overload
	def closeAndDrop(self) -> "Inventory":
		pass

	@overload
	def close(self) -> None:
		pass

	@overload
	def quick(self, slot: int) -> "Inventory":
		pass

	@overload
	def getHeld(self) -> ItemStackHelper:
		pass

	@overload
	def getSlot(self, slot: int) -> ItemStackHelper:
		pass

	@overload
	def getTotalSlots(self) -> int:
		pass

	@overload
	def split(self, slot1: int, slot2: int) -> "Inventory":
		pass

	@overload
	def grabAll(self, slot: int) -> "Inventory":
		pass

	@overload
	def swap(self, slot1: int, slot2: int) -> "Inventory":
		pass

	@overload
	def openGui(self) -> None:
		pass

	@overload
	def getSlotUnderMouse(self) -> int:
		pass

	@overload
	def getType(self) -> str:
		pass

	@overload
	def getMap(self) -> Mapping[str, List[int]]:
		pass

	@overload
	def getLocation(self, slotNum: int) -> str:
		pass

	@overload
	def getCraftableRecipes(self) -> List[RecipeHelper]:
		pass

	@overload
	def getContainerTitle(self) -> str:
		pass

	@overload
	def getRawContainer(self) -> T:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



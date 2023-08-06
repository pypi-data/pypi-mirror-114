from typing import overload
from .Inventory import Inventory


class BeaconInventory(Inventory):

	@overload
	def getLevel(self) -> int:
		pass

	@overload
	def getFirstEffect(self) -> str:
		pass

	@overload
	def getSecondEffect(self) -> str:
		pass

	@overload
	def selectFirstEffect(self, id: str) -> bool:
		pass

	@overload
	def selectSecondEffect(self, id: str) -> bool:
		pass

	@overload
	def applyEffects(self) -> bool:
		pass

	pass



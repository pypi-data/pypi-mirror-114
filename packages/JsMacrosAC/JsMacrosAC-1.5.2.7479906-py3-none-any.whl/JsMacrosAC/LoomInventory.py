from typing import overload
from .Inventory import Inventory


class LoomInventory(Inventory):

	@overload
	def selectPatternName(self, name: str) -> bool:
		pass

	@overload
	def selectPatternId(self, id: str) -> bool:
		pass

	@overload
	def selectPattern(self, index: int) -> bool:
		pass

	pass



from typing import overload
from typing import List
from .Inventory import *
from .TextHelper import *


class EnchantInventory(Inventory):

	@overload
	def getRequiredLevels(self) -> List[int]:
		pass

	@overload
	def getEnchantments(self) -> List[TextHelper]:
		pass

	@overload
	def getEnchantmentIds(self) -> List[str]:
		pass

	@overload
	def getEnchantmentLevels(self) -> List[int]:
		pass

	@overload
	def doEnchant(self, index: int) -> bool:
		pass

	pass



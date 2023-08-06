from typing import overload
from typing import List
from .Inventory import Inventory
from .TradeOfferHelper import TradeOfferHelper


class VillagerInventory(Inventory):

	@overload
	def selectTrade(self, index: int) -> "VillagerInventory":
		pass

	@overload
	def getExperience(self) -> int:
		pass

	@overload
	def getLevelProgress(self) -> int:
		pass

	@overload
	def getMerchantRewardedExperience(self) -> int:
		pass

	@overload
	def canRefreshTrades(self) -> bool:
		pass

	@overload
	def isLeveled(self) -> bool:
		pass

	@overload
	def getTrades(self) -> List[TradeOfferHelper]:
		pass

	pass



from typing import overload
from typing import List
from typing import TypeVar
from .Inventory import *
from .VillagerInventory import *
from .TradeOfferHelper import *

List = TypeVar["java.util.List_xyz.wagyourtail.jsmacros.client.api.helpers.TradeOfferHelper_"]

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



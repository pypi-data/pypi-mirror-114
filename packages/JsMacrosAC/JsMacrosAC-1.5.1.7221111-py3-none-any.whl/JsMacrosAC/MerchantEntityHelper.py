from typing import overload
from typing import List
from typing import TypeVar
from .LivingEntityHelper import *
from .TradeOfferHelper import *

MerchantEntity = TypeVar["net.minecraft.entity.passive.MerchantEntity"]
List = TypeVar["java.util.List_xyz.wagyourtail.jsmacros.client.api.helpers.TradeOfferHelper_"]

class MerchantEntityHelper(LivingEntityHelper):

	@overload
	def __init__(self, e: MerchantEntity) -> None:
		pass

	@overload
	def getTrades(self) -> List[TradeOfferHelper]:
		pass

	@overload
	def getExperience(self) -> int:
		pass

	@overload
	def hasCustomer(self) -> bool:
		pass

	pass



from typing import overload
from typing import List
from typing import TypeVar
from .LivingEntityHelper import LivingEntityHelper
from .TradeOfferHelper import TradeOfferHelper

MerchantEntity = TypeVar["net.minecraft.entity.passive.MerchantEntity"]

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



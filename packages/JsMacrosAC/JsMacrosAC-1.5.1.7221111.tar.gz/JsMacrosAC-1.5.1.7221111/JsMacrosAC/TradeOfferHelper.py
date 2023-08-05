from typing import overload
from typing import List
from typing import TypeVar
from .BaseHelper import *
from .VillagerInventory import *
from .ItemStackHelper import *
from .NBTElementHelper import *

List = TypeVar["java.util.List_xyz.wagyourtail.jsmacros.client.api.helpers.ItemStackHelper_"]
TradeOffer = TypeVar["net.minecraft.village.TradeOffer"]

class TradeOfferHelper(BaseHelper):

	@overload
	def __init__(self, base: TradeOffer, index: int, inv: VillagerInventory) -> None:
		pass

	@overload
	def getInput(self) -> List[ItemStackHelper]:
		pass

	@overload
	def getOutput(self) -> ItemStackHelper:
		pass

	@overload
	def select(self) -> None:
		pass

	@overload
	def isAvailable(self) -> bool:
		pass

	@overload
	def getNBT(self) -> NBTElementHelper:
		pass

	@overload
	def getUses(self) -> int:
		pass

	@overload
	def getMaxUses(self) -> int:
		pass

	@overload
	def getExperience(self) -> int:
		pass

	@overload
	def getCurrentPriceAdjustment(self) -> int:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



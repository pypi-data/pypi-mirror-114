from typing import overload
from .IMerchantScreen import *


class MixinMerchantScreen(IMerchantScreen):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def jsmacros_selectIndex(self, index: int) -> None:
		pass

	pass



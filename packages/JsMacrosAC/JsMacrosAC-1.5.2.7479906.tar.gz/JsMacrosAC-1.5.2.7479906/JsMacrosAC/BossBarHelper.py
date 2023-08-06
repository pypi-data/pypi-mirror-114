from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper
from .TextHelper import TextHelper

BossBar = TypeVar["net.minecraft.entity.boss.BossBar"]

class BossBarHelper(BaseHelper):

	@overload
	def __init__(self, b: BossBar) -> None:
		pass

	@overload
	def getUUID(self) -> str:
		pass

	@overload
	def getPercent(self) -> float:
		pass

	@overload
	def getColor(self) -> str:
		pass

	@overload
	def getStyle(self) -> str:
		pass

	@overload
	def getName(self) -> TextHelper:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



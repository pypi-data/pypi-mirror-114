from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper
from .TextHelper import TextHelper

PlayerListEntry = TypeVar["net.minecraft.client.network.PlayerListEntry"]

class PlayerListEntryHelper(BaseHelper):

	@overload
	def __init__(self, p: PlayerListEntry) -> None:
		pass

	@overload
	def getUUID(self) -> str:
		pass

	@overload
	def getName(self) -> str:
		pass

	@overload
	def getDisplayText(self) -> TextHelper:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



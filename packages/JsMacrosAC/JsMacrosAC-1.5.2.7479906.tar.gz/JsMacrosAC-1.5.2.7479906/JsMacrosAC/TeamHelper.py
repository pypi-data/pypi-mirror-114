from typing import overload
from typing import List
from typing import TypeVar
from .BaseHelper import BaseHelper
from .TextHelper import TextHelper

Team = TypeVar["net.minecraft.scoreboard.Team"]

class TeamHelper(BaseHelper):

	@overload
	def __init__(self, t: Team) -> None:
		pass

	@overload
	def getName(self) -> str:
		pass

	@overload
	def getDisplayName(self) -> TextHelper:
		pass

	@overload
	def getPlayerList(self) -> List[str]:
		pass

	@overload
	def getColor(self) -> int:
		pass

	@overload
	def getPrefix(self) -> TextHelper:
		pass

	@overload
	def getSuffix(self) -> TextHelper:
		pass

	@overload
	def getCollisionRule(self) -> str:
		pass

	@overload
	def isFriendlyFire(self) -> bool:
		pass

	@overload
	def showFriendlyInvisibles(self) -> bool:
		pass

	@overload
	def nametagVisibility(self) -> str:
		pass

	@overload
	def deathMessageVisibility(self) -> str:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



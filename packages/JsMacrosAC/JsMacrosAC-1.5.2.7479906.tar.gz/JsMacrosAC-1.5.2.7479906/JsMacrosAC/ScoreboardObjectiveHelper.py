from typing import overload
from typing import TypeVar
from typing import Mapping
from .BaseHelper import BaseHelper
from .TextHelper import TextHelper

ScoreboardObjective = TypeVar["net.minecraft.scoreboard.ScoreboardObjective"]

class ScoreboardObjectiveHelper(BaseHelper):

	@overload
	def __init__(self, o: ScoreboardObjective) -> None:
		pass

	@overload
	def getPlayerScores(self) -> Mapping[str, int]:
		pass

	@overload
	def getName(self) -> str:
		pass

	@overload
	def getDisplayName(self) -> TextHelper:
		pass

	pass



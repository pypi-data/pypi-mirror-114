from typing import overload
from typing import List
from typing import TypeVar
from .BaseHelper import *
from .ScoreboardObjectiveHelper import *
from .PlayerEntityHelper import *
from .TeamHelper import *

Scoreboard = TypeVar["net.minecraft.scoreboard.Scoreboard"]
List = TypeVar["java.util.List_xyz.wagyourtail.jsmacros.client.api.helpers.TeamHelper_"]

class ScoreboardsHelper(BaseHelper):

	@overload
	def __init__(self, board: Scoreboard) -> None:
		pass

	@overload
	def getObjectiveForTeamColorIndex(self, index: int) -> ScoreboardObjectiveHelper:
		pass

	@overload
	def getObjectiveSlot(self, slot: int) -> ScoreboardObjectiveHelper:
		pass

	@overload
	def getPlayerTeamColorIndex(self, entity: PlayerEntityHelper) -> int:
		pass

	@overload
	def getTeams(self) -> List[TeamHelper]:
		pass

	@overload
	def getPlayerTeam(self, p: PlayerEntityHelper) -> TeamHelper:
		pass

	@overload
	def getCurrentScoreboard(self) -> ScoreboardObjectiveHelper:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



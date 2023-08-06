from typing import overload
from typing import List
from typing import Mapping
from .BaseLibrary import BaseLibrary
from .PlayerEntityHelper import PlayerEntityHelper
from .PlayerListEntryHelper import PlayerListEntryHelper
from .BlockDataHelper import BlockDataHelper
from .ScoreboardsHelper import ScoreboardsHelper
from .EntityHelper import EntityHelper
from .BlockPosHelper import BlockPosHelper
from .BossBarHelper import BossBarHelper
from .TextHelper import TextHelper


class FWorld(BaseLibrary):
	serverInstantTPS: float
	server1MAverageTPS: float
	server5MAverageTPS: float
	server15MAverageTPS: float

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def isWorldLoaded(self) -> bool:
		pass

	@overload
	def getLoadedPlayers(self) -> List[PlayerEntityHelper]:
		pass

	@overload
	def getPlayers(self) -> List[PlayerListEntryHelper]:
		pass

	@overload
	def getBlock(self, x: int, y: int, z: int) -> BlockDataHelper:
		pass

	@overload
	def getScoreboards(self) -> ScoreboardsHelper:
		pass

	@overload
	def getEntities(self) -> List[EntityHelper]:
		pass

	@overload
	def getDimension(self) -> str:
		pass

	@overload
	def getBiome(self) -> str:
		pass

	@overload
	def getTime(self) -> float:
		pass

	@overload
	def getTimeOfDay(self) -> float:
		pass

	@overload
	def getRespawnPos(self) -> BlockPosHelper:
		pass

	@overload
	def getDifficulty(self) -> int:
		pass

	@overload
	def getMoonPhase(self) -> int:
		pass

	@overload
	def getSkyLight(self, x: int, y: int, z: int) -> int:
		pass

	@overload
	def getBlockLight(self, x: int, y: int, z: int) -> int:
		pass

	@overload
	def playSoundFile(self, file: str, volume: float) -> Clip:
		pass

	@overload
	def playSound(self, id: str) -> None:
		pass

	@overload
	def playSound(self, id: str, volume: float) -> None:
		pass

	@overload
	def playSound(self, id: str, volume: float, pitch: float) -> None:
		pass

	@overload
	def playSound(self, id: str, volume: float, pitch: float, x: float, y: float, z: float) -> None:
		pass

	@overload
	def getBossBars(self) -> Mapping[str, BossBarHelper]:
		pass

	@overload
	def isChunkLoaded(self, chunkX: int, chunkZ: int) -> bool:
		pass

	@overload
	def getCurrentServerAddress(self) -> str:
		pass

	@overload
	def getBiomeAt(self, x: int, z: int) -> str:
		pass

	@overload
	def getServerTPS(self) -> str:
		pass

	@overload
	def getTabListHeader(self) -> TextHelper:
		pass

	@overload
	def getTabListFooter(self) -> TextHelper:
		pass

	@overload
	def getServerInstantTPS(self) -> float:
		pass

	@overload
	def getServer1MAverageTPS(self) -> float:
		pass

	@overload
	def getServer5MAverageTPS(self) -> float:
		pass

	@overload
	def getServer15MAverageTPS(self) -> float:
		pass

	pass



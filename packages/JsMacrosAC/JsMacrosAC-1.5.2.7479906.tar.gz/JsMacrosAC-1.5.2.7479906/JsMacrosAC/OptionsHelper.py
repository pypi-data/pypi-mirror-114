from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from .BaseHelper import BaseHelper

GameOptions = TypeVar["net.minecraft.client.option.GameOptions"]

class OptionsHelper(BaseHelper):

	@overload
	def __init__(self, options: GameOptions) -> None:
		pass

	@overload
	def getCloudMode(self) -> int:
		pass

	@overload
	def setCloudMode(self, mode: int) -> "OptionsHelper":
		pass

	@overload
	def getGraphicsMode(self) -> int:
		pass

	@overload
	def setGraphicsMode(self, mode: int) -> "OptionsHelper":
		pass

	@overload
	def getResourcePacks(self) -> List[str]:
		pass

	@overload
	def getEnabledResourcePacks(self) -> List[str]:
		pass

	@overload
	def setEnabledResourcePacks(self, enabled: List[str]) -> "OptionsHelper":
		pass

	@overload
	def isRightHanded(self) -> bool:
		pass

	@overload
	def setRightHanded(self, val: bool) -> None:
		pass

	@overload
	def getFov(self) -> float:
		pass

	@overload
	def setFov(self, fov: float) -> "OptionsHelper":
		pass

	@overload
	def getRenderDistance(self) -> int:
		pass

	@overload
	def setRenderDistance(self, d: int) -> None:
		pass

	@overload
	def getWidth(self) -> int:
		pass

	@overload
	def getHeight(self) -> int:
		pass

	@overload
	def setWidth(self, w: int) -> None:
		pass

	@overload
	def setHeight(self, h: int) -> None:
		pass

	@overload
	def setSize(self, w: int, h: int) -> None:
		pass

	@overload
	def getGamma(self) -> float:
		pass

	@overload
	def setGamma(self, gamma: float) -> None:
		pass

	@overload
	def setVolume(self, vol: float) -> None:
		pass

	@overload
	def setVolume(self, category: str, volume: float) -> None:
		pass

	@overload
	def getVolumes(self) -> Mapping[str, Float]:
		pass

	@overload
	def setGuiScale(self, scale: int) -> None:
		pass

	@overload
	def getGuiScale(self) -> int:
		pass

	@overload
	def getVolume(self, category: str) -> float:
		pass

	@overload
	def getSmoothCamera(self) -> bool:
		pass

	@overload
	def setSmoothCamera(self, val: bool) -> None:
		pass

	@overload
	def getCameraMode(self) -> int:
		pass

	@overload
	def setCameraMode(self, mode: int) -> None:
		pass

	pass



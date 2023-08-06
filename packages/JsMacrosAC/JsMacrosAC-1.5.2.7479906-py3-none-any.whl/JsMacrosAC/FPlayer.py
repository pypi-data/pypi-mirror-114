from typing import overload
from typing import List
from .BaseLibrary import BaseLibrary
from .Inventory import Inventory
from .ClientPlayerEntityHelper import ClientPlayerEntityHelper
from .BlockDataHelper import BlockDataHelper
from .EntityHelper import EntityHelper
from .MethodWrapper import MethodWrapper
from .PlayerInput import PlayerInput
from .PositionCommon_Pos3D import PositionCommon_Pos3D


class FPlayer(BaseLibrary):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def openInventory(self) -> Inventory:
		pass

	@overload
	def getPlayer(self) -> ClientPlayerEntityHelper:
		pass

	@overload
	def getGameMode(self) -> str:
		pass

	@overload
	def rayTraceBlock(self, distance: float, fluid: bool) -> BlockDataHelper:
		pass

	@overload
	def rayTraceEntity(self) -> EntityHelper:
		pass

	@overload
	def writeSign(self, l1: str, l2: str, l3: str, l4: str) -> bool:
		pass

	@overload
	def takeScreenshot(self, folder: str, callback: MethodWrapper) -> None:
		pass

	@overload
	def takeScreenshot(self, folder: str, file: str, callback: MethodWrapper) -> None:
		pass

	@overload
	def createPlayerInput(self) -> PlayerInput:
		pass

	@overload
	def createPlayerInput(self, movementForward: float, movementSideways: float, yaw: float) -> PlayerInput:
		pass

	@overload
	def createPlayerInput(self, movementForward: float, yaw: float, jumping: bool, sprinting: bool) -> PlayerInput:
		pass

	@overload
	def createPlayerInput(self, movementForward: float, movementSideways: float, yaw: float, pitch: float, jumping: bool, sneaking: bool, sprinting: bool) -> PlayerInput:
		pass

	@overload
	def createPlayerInputsFromCsv(self, csv: str) -> List[PlayerInput]:
		pass

	@overload
	def createPlayerInputsFromJson(self, json: str) -> PlayerInput:
		pass

	@overload
	def getCurrentPlayerInput(self) -> PlayerInput:
		pass

	@overload
	def addInput(self, input: PlayerInput) -> None:
		pass

	@overload
	def addInputs(self, inputs: List[PlayerInput]) -> None:
		pass

	@overload
	def clearInputs(self) -> None:
		pass

	@overload
	def setDrawPredictions(self, val: bool) -> None:
		pass

	@overload
	def predictInput(self, input: PlayerInput) -> PositionCommon_Pos3D:
		pass

	@overload
	def predictInput(self, input: PlayerInput, draw: bool) -> PositionCommon_Pos3D:
		pass

	@overload
	def predictInputs(self, inputs: List[PlayerInput]) -> List[PositionCommon_Pos3D]:
		pass

	@overload
	def predictInputs(self, inputs: List[PlayerInput], draw: bool) -> List[PositionCommon_Pos3D]:
		pass

	@overload
	def moveForward(self, yaw: float) -> None:
		pass

	@overload
	def moveBackward(self, yaw: float) -> None:
		pass

	@overload
	def moveStrafeLeft(self, yaw: float) -> None:
		pass

	@overload
	def moveStrafeRight(self, yaw: float) -> None:
		pass

	pass



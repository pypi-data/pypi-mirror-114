from typing import overload
from typing import List
from typing import TypeVar
from typing import Generic
from .BaseHelper import BaseHelper
from .PositionCommon_Pos3D import PositionCommon_Pos3D
from .NBTElementHelper import NBTElementHelper

Entity = TypeVar["net.minecraft.entity.Entity"]
T = TypeVar("T")

class EntityHelper(Generic[T], BaseHelper):

	@overload
	def __init__(self, e: T) -> None:
		pass

	@overload
	def getPos(self) -> PositionCommon_Pos3D:
		pass

	@overload
	def getX(self) -> float:
		pass

	@overload
	def getY(self) -> float:
		pass

	@overload
	def getZ(self) -> float:
		pass

	@overload
	def getEyeHeight(self) -> float:
		pass

	@overload
	def getPitch(self) -> float:
		pass

	@overload
	def getYaw(self) -> float:
		pass

	@overload
	def getName(self) -> str:
		pass

	@overload
	def getType(self) -> str:
		pass

	@overload
	def isGlowing(self) -> bool:
		pass

	@overload
	def isInLava(self) -> bool:
		pass

	@overload
	def isOnFire(self) -> bool:
		pass

	@overload
	def getVehicle(self) -> "EntityHelper":
		pass

	@overload
	def getPassengers(self) -> List["EntityHelper"]:
		pass

	@overload
	def getNBT(self) -> NBTElementHelper:
		pass

	@overload
	def setGlowing(self, val: bool) -> "EntityHelper":
		pass

	@overload
	def isAlive(self) -> bool:
		pass

	@overload
	def toString(self) -> str:
		pass

	@overload
	def create(self, e: Entity) -> "EntityHelper":
		pass

	pass



from typing import overload
from typing import List
from typing import TypeVar
from .BaseHelper import *
from .PositionCommon_Pos3D import *
from .EntityHelper import *
from .NBTElementHelper import *

Entity = TypeVar["net.minecraft.entity.Entity"]
T = TypeVar["T"]
List = TypeVar["java.util.List_xyz.wagyourtail.jsmacros.client.api.helpers.EntityHelper___"]

class EntityHelper(BaseHelper):

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



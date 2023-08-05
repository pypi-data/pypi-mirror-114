from typing import overload
from typing import TypeVar
from .BaseHelper import *
from .NBTElementHelper_NBTNumberHelper import *
from .NBTElementHelper_NBTListHelper import *
from .NBTElementHelper_NBTCompoundHelper import *
from .NBTElementHelper import *

NbtElement = TypeVar["net.minecraft.nbt.NbtElement"]

class NBTElementHelper(BaseHelper):

	@overload
	def getType(self) -> int:
		pass

	@overload
	def isNull(self) -> bool:
		pass

	@overload
	def isNumber(self) -> bool:
		pass

	@overload
	def isString(self) -> bool:
		pass

	@overload
	def isList(self) -> bool:
		pass

	@overload
	def isCompound(self) -> bool:
		pass

	@overload
	def asString(self) -> str:
		pass

	@overload
	def asNumberHelper(self) -> NBTElementHelper_NBTNumberHelper:
		pass

	@overload
	def asListHelper(self) -> NBTElementHelper_NBTListHelper:
		pass

	@overload
	def asCompoundHelper(self) -> NBTElementHelper_NBTCompoundHelper:
		pass

	@overload
	def toString(self) -> str:
		pass

	@overload
	def resolve(self, element: NbtElement) -> "NBTElementHelper":
		pass

	pass



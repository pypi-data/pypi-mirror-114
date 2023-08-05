from typing import overload
from .NBTElementHelper import *


class NBTElementHelper_NBTCompoundHelper(NBTElementHelper):

	@overload
	def getType(self, key: str) -> int:
		pass

	@overload
	def has(self, key: str) -> bool:
		pass

	@overload
	def get(self, key: str) -> NBTElementHelper:
		pass

	@overload
	def asString(self, key: str) -> str:
		pass

	pass



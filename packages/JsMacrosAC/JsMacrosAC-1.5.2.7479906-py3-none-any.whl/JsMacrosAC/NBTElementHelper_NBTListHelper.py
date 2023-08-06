from typing import overload
from .NBTElementHelper import NBTElementHelper


class NBTElementHelper_NBTListHelper(NBTElementHelper):

	@overload
	def length(self) -> int:
		pass

	@overload
	def get(self, index: int) -> NBTElementHelper:
		pass

	@overload
	def getHeldType(self) -> int:
		pass

	pass



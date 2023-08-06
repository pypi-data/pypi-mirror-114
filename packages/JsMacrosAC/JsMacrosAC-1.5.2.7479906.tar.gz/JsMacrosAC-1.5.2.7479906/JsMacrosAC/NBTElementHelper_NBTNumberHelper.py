from typing import overload
from .NBTElementHelper import NBTElementHelper


class NBTElementHelper_NBTNumberHelper(NBTElementHelper):

	@overload
	def asLong(self) -> float:
		pass

	@overload
	def asInt(self) -> int:
		pass

	@overload
	def asShort(self) -> float:
		pass

	@overload
	def asByte(self) -> float:
		pass

	@overload
	def asFloat(self) -> float:
		pass

	@overload
	def asDouble(self) -> float:
		pass

	@overload
	def asNumber(self) -> Number:
		pass

	pass



from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper

BlockPos = TypeVar["net.minecraft.util.math.BlockPos"]

class BlockPosHelper(BaseHelper):

	@overload
	def __init__(self, b: BlockPos) -> None:
		pass

	@overload
	def getX(self) -> int:
		pass

	@overload
	def getY(self) -> int:
		pass

	@overload
	def getZ(self) -> int:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



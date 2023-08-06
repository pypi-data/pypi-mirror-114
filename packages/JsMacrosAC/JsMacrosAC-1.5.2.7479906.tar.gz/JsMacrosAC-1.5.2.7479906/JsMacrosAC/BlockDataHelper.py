from typing import overload
from typing import TypeVar
from typing import Mapping
from .BaseHelper import BaseHelper
from .NBTElementHelper import NBTElementHelper
from .BlockPosHelper import BlockPosHelper

BlockState = TypeVar["net.minecraft.block.BlockState"]
Block = TypeVar["net.minecraft.block.Block"]
BlockPos = TypeVar["net.minecraft.util.math.BlockPos"]
BlockEntity = TypeVar["net.minecraft.block.entity.BlockEntity"]

class BlockDataHelper(BaseHelper):

	@overload
	def __init__(self, b: BlockState, e: BlockEntity, bp: BlockPos) -> None:
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
	def getId(self) -> str:
		pass

	@overload
	def getName(self) -> str:
		pass

	@overload
	def getNBT(self) -> NBTElementHelper:
		pass

	@overload
	def getBlockState(self) -> Mapping[str, str]:
		pass

	@overload
	def getBlockPos(self) -> BlockPosHelper:
		pass

	@overload
	def getRawBlock(self) -> Block:
		pass

	@overload
	def getRawBlockState(self) -> BlockState:
		pass

	@overload
	def getRawBlockEntity(self) -> BlockEntity:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



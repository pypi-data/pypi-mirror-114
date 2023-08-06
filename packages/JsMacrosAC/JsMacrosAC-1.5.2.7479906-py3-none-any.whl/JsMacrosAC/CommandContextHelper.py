from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper

CommandContext = TypeVar["com.mojang.brigadier.context.CommandContext_net.fabricmc.fabric.api.client.command.v1.FabricClientCommandSource_"]
StringRange = TypeVar["com.mojang.brigadier.context.StringRange"]

class CommandContextHelper(BaseHelper):

	@overload
	def __init__(self, base: CommandContext) -> None:
		pass

	@overload
	def getArg(self, name: str) -> object:
		pass

	@overload
	def getChild(self) -> "CommandContextHelper":
		pass

	@overload
	def getRange(self) -> StringRange:
		pass

	@overload
	def getInput(self) -> str:
		pass

	pass



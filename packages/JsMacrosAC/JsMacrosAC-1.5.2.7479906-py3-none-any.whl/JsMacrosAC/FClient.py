from typing import overload
from typing import TypeVar
from .BaseLibrary import BaseLibrary
from .TickSync import TickSync
from .MethodWrapper import MethodWrapper
from .OptionsHelper import OptionsHelper

MinecraftClient = TypeVar["net.minecraft.client.MinecraftClient"]

class FClient(BaseLibrary):
	tickSynchronizer: TickSync

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def getMinecraft(self) -> MinecraftClient:
		pass

	@overload
	def runOnMainThread(self, runnable: MethodWrapper) -> None:
		pass

	@overload
	def getGameOptions(self) -> OptionsHelper:
		pass

	@overload
	def mcVersion(self) -> str:
		pass

	@overload
	def getFPS(self) -> str:
		pass

	@overload
	def connect(self, ip: str) -> None:
		pass

	@overload
	def connect(self, ip: str, port: int) -> None:
		pass

	@overload
	def disconnect(self) -> None:
		pass

	@overload
	def disconnect(self, callback: MethodWrapper) -> None:
		pass

	@overload
	def shutdown(self) -> None:
		pass

	@overload
	def waitTick(self) -> None:
		pass

	@overload
	def waitTick(self, i: int) -> None:
		pass

	pass



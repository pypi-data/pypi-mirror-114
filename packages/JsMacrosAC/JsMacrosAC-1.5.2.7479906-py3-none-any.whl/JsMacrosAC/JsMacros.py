from typing import overload
from typing import List
from typing import TypeVar
from .BaseScreen import BaseScreen
from .Core import Core

KeyBinding = TypeVar["net.minecraft.client.option.KeyBinding"]
Screen = TypeVar["net.minecraft.client.gui.screen.Screen"]
MinecraftClient = TypeVar["net.minecraft.client.MinecraftClient"]
InputUtil_Key = TypeVar["net.minecraft.client.util.InputUtil.Key"]
ClientModInitializer = TypeVar["net.fabricmc.api.ClientModInitializer"]
Text = TypeVar["net.minecraft.text.Text"]
Logger = TypeVar["org.apache.logging.log4j.Logger"]

class JsMacros(ClientModInitializer):
	MOD_ID: str
	LOGGER: Logger
	keyBinding: KeyBinding
	prevScreen: BaseScreen
	core: Core

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def onInitializeClient(self) -> None:
		pass

	@overload
	def getKeyText(self, translationKey: str) -> Text:
		pass

	@overload
	def getScreenName(self, s: Screen) -> str:
		pass

	@overload
	def getLocalizedName(self, keyCode: InputUtil_Key) -> str:
		pass

	@overload
	def getMinecraft(self) -> MinecraftClient:
		pass

	@overload
	def range(self, end: int) -> List[int]:
		pass

	@overload
	def range(self, start: int, end: int) -> List[int]:
		pass

	@overload
	def range(self, start: int, end: int, iter: int) -> List[int]:
		pass

	pass



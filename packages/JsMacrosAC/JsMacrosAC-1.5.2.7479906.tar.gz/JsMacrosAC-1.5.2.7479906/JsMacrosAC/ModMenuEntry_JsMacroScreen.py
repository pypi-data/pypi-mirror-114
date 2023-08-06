from typing import overload
from typing import TypeVar
from .BaseScreen import BaseScreen

Screen = TypeVar["net.minecraft.client.gui.screen.Screen"]
ConfigScreenFactory = TypeVar["com.terraformersmc.modmenu.api.ConfigScreenFactory_xyz.wagyourtail.jsmacros.client.gui.screens.BaseScreen_"]

class ModMenuEntry_JsMacroScreen(ConfigScreenFactory):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def create(self, parent: Screen) -> BaseScreen:
		pass

	pass



from typing import overload
from typing import TypeVar

ModMenuApi = TypeVar["com.terraformersmc.modmenu.api.ModMenuApi"]
ConfigScreenFactory = TypeVar["com.terraformersmc.modmenu.api.ConfigScreenFactory__"]

class ModMenuEntry(ModMenuApi):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def getModConfigScreenFactory(self) -> ConfigScreenFactory:
		pass

	pass



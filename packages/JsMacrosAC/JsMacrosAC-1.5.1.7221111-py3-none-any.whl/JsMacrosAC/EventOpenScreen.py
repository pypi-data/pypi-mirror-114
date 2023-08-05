from typing import overload
from typing import TypeVar
from .BaseEvent import *
from .IScreen import *

Screen = TypeVar["net.minecraft.client.gui.screen.Screen"]

class EventOpenScreen(BaseEvent):
	screen: IScreen
	screenName: str

	@overload
	def __init__(self, screen: Screen) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



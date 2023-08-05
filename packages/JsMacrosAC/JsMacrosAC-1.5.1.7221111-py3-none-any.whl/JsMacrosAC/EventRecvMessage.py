from typing import overload
from typing import TypeVar
from .BaseEvent import *
from .TextHelper import *

Text = TypeVar["net.minecraft.text.Text"]

class EventRecvMessage(BaseEvent):
	text: TextHelper

	@overload
	def __init__(self, message: Text) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



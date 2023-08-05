from typing import overload
from typing import TypeVar
from .BaseEvent import *
from .ClientPlayerEntityHelper import *

ClientPlayerEntity = TypeVar["net.minecraft.client.network.ClientPlayerEntity"]

class EventJoinServer(BaseEvent):
	player: ClientPlayerEntityHelper
	address: str

	@overload
	def __init__(self, player: ClientPlayerEntity, address: str) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



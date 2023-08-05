from typing import overload
from typing import TypeVar
from .BaseProfile import *
from .Core import *
from .BaseEvent import *

Throwable = TypeVar["java.lang.Throwable"]

class Profile(BaseProfile):

	@overload
	def __init__(self, runner: Core) -> None:
		pass

	@overload
	def triggerEventJoin(self, event: BaseEvent) -> None:
		pass

	@overload
	def triggerEventJoinNoAnything(self, event: BaseEvent) -> None:
		pass

	@overload
	def logError(self, ex: Throwable) -> None:
		pass

	@overload
	def initRegistries(self) -> None:
		pass

	pass



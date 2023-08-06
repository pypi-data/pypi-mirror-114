from typing import overload
from typing import TypeVar
from .EventContainer import EventContainer
from .IEventListener import IEventListener

Thread = TypeVar["java.lang.Thread"]

class EventLockWatchdog:

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def startWatchdog(self, lock: EventContainer, watched: Thread, listener: IEventListener, maxTime: float) -> None:
		pass

	pass



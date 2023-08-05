from typing import overload
from typing import TypeVar
from .ContextContainer import *
from .IEventListener import *

Thread = TypeVar["java.lang.Thread"]

class ContextLockWatchdog:

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def startWatchdog(self, lock: ContextContainer, watched: Thread, listener: IEventListener, maxTime: float) -> None:
		pass

	pass



from typing import overload
from typing import TypeVar
from typing import Generic
from .BaseScriptContext import BaseScriptContext

T = TypeVar("T")
Runnable = TypeVar["java.lang.Runnable"]
Thread = TypeVar["java.lang.Thread"]

class EventContainer(Generic[T]):

	@overload
	def __init__(self, ctx: BaseScriptContext) -> None:
		pass

	@overload
	def isLocked(self) -> bool:
		pass

	@overload
	def setLockThread(self, lockThread: Thread) -> None:
		pass

	@overload
	def getCtx(self) -> BaseScriptContext:
		pass

	@overload
	def getLockThread(self) -> Thread:
		pass

	@overload
	def awaitLock(self, then: Runnable) -> None:
		pass

	@overload
	def releaseLock(self) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



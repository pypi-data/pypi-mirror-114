from typing import overload
from typing import TypeVar
from typing import Mapping
from typing import Set
from typing import Generic
from .BaseEvent import BaseEvent
from .EventContainer import EventContainer

T = TypeVar("T")
File = TypeVar["java.io.File"]
Thread = TypeVar["java.lang.Thread"]

class BaseScriptContext(Generic[T]):
	startTime: float
	triggeringEvent: BaseEvent
	events: Mapping[Thread, EventContainer]
	hasMethodWrapperBeenInvoked: bool

	@overload
	def __init__(self, event: BaseEvent, file: File) -> None:
		pass

	@overload
	def getContext(self) -> T:
		pass

	@overload
	def getMainThread(self) -> Thread:
		pass

	@overload
	def bindThread(self, t: Thread) -> bool:
		pass

	@overload
	def unbindThread(self, t: Thread) -> None:
		pass

	@overload
	def getBoundThreads(self) -> Set[Thread]:
		pass

	@overload
	def setMainThread(self, t: Thread) -> None:
		pass

	@overload
	def getTriggeringEvent(self) -> BaseEvent:
		pass

	@overload
	def setContext(self, context: T) -> None:
		pass

	@overload
	def isContextClosed(self) -> bool:
		pass

	@overload
	def closeContext(self) -> None:
		pass

	@overload
	def getFile(self) -> File:
		pass

	@overload
	def getContainedFolder(self) -> File:
		pass

	pass



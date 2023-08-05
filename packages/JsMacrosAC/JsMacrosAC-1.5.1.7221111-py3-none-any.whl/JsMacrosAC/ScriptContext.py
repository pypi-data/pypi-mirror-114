from typing import overload
from typing import TypeVar
from .BaseEvent import *

T = TypeVar["T"]
WeakReference = TypeVar["java.lang.ref.WeakReference_java.lang.Thread_"]
Thread = TypeVar["java.lang.Thread"]

class ScriptContext:
	startTime: float

	@overload
	def __init__(self, event: BaseEvent) -> None:
		pass

	@overload
	def getContext(self) -> WeakReference:
		pass

	@overload
	def getMainThread(self) -> WeakReference:
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

	pass



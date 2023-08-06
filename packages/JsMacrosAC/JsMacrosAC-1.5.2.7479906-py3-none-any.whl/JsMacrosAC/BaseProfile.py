from typing import overload
from typing import TypeVar
from typing import Set
from .Core import Core
from .BaseEventRegistry import BaseEventRegistry
from .BaseEvent import BaseEvent

Throwable = TypeVar["java.lang.Throwable"]
Logger = TypeVar["org.apache.logging.log4j.Logger"]
Thread = TypeVar["java.lang.Thread"]

class BaseProfile:
	LOGGER: Logger
	joinedThreadStack: Set[Thread]
	profileName: str

	@overload
	def __init__(self, runner: Core, logger: Logger) -> None:
		pass

	@overload
	def logError(self, ex: Throwable) -> None:
		pass

	@overload
	def getRegistry(self) -> BaseEventRegistry:
		pass

	@overload
	def loadOrCreateProfile(self, profileName: str) -> None:
		pass

	@overload
	def saveProfile(self) -> None:
		pass

	@overload
	def triggerEvent(self, event: BaseEvent) -> None:
		pass

	@overload
	def triggerEventJoin(self, event: BaseEvent) -> None:
		pass

	@overload
	def triggerEventNoAnything(self, event: BaseEvent) -> None:
		pass

	@overload
	def triggerEventJoinNoAnything(self, event: BaseEvent) -> None:
		pass

	@overload
	def init(self, defaultProfile: str) -> None:
		pass

	@overload
	def getCurrentProfileName(self) -> str:
		pass

	@overload
	def renameCurrentProfile(self, profile: str) -> None:
		pass

	pass



from typing import overload
from .BaseProfile import *


class BaseEvent:
	profile: BaseProfile

	@overload
	def getEventName(self) -> str:
		pass

	pass



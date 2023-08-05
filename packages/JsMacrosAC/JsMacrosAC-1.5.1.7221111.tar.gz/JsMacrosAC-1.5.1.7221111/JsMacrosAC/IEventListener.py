from typing import overload
from .BaseEvent import *
from .ContextContainer import *


class IEventListener:

	@overload
	def trigger(self, event: BaseEvent) -> ContextContainer:
		pass

	pass



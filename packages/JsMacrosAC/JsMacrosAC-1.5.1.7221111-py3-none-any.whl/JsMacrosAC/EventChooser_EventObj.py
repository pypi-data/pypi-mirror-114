from typing import overload
from .Button import *


class EventChooser_EventObj:

	@overload
	def __init__(self, event: str, btn: Button) -> None:
		pass

	pass



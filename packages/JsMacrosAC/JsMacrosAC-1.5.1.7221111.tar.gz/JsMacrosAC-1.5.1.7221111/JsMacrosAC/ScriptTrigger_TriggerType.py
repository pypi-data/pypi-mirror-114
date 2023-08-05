from typing import overload
from typing import List
from .ScriptTrigger_TriggerType import *


class ScriptTrigger_TriggerType:
	KEY_FALLING: "ScriptTrigger_TriggerType"
	KEY_RISING: "ScriptTrigger_TriggerType"
	KEY_BOTH: "ScriptTrigger_TriggerType"
	EVENT: "ScriptTrigger_TriggerType"

	@overload
	def values(self) -> List["ScriptTrigger_TriggerType"]:
		pass

	@overload
	def valueOf(self, name: str) -> "ScriptTrigger_TriggerType":
		pass

	pass



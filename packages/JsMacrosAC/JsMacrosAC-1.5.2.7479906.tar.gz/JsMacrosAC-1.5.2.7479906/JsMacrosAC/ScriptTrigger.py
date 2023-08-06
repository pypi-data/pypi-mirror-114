from typing import overload
from .ScriptTrigger_TriggerType import ScriptTrigger_TriggerType


class ScriptTrigger:
	triggerType: ScriptTrigger_TriggerType
	event: str
	scriptFile: str
	enabled: bool

	@overload
	def __init__(self, triggerType: ScriptTrigger_TriggerType, event: str, scriptFile: str, enabled: bool) -> None:
		pass

	@overload
	def equals(self, macro: "ScriptTrigger") -> bool:
		pass

	@overload
	def toString(self) -> str:
		pass

	@overload
	def copy(self, m: "ScriptTrigger") -> "ScriptTrigger":
		pass

	@overload
	def copy(self) -> "ScriptTrigger":
		pass

	@overload
	def getTriggerType(self) -> ScriptTrigger_TriggerType:
		pass

	@overload
	def getEvent(self) -> str:
		pass

	@overload
	def getScriptFile(self) -> str:
		pass

	@overload
	def getEnabled(self) -> bool:
		pass

	pass



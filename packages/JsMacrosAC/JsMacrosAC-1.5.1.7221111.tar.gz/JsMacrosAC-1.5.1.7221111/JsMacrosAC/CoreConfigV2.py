from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from .ScriptTrigger import *

JsonObject = TypeVar["com.google.gson.JsonObject"]
List = TypeVar["java.util.List_java.lang.String_"]
Map = TypeVar["java.util.Map_java.lang.String,java.lang.String_"]

class CoreConfigV2:
	maxLockTime: float
	defaultProfile: str
	profiles: Mapping[str, List[ScriptTrigger]]
	extraJsOptions: Mapping[str, str]

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def getCurrentProfile(self) -> str:
		pass

	@overload
	def setCurrentProfile(self, pname: str) -> None:
		pass

	@overload
	def profileOptions(self) -> List[str]:
		pass

	@overload
	def fromV1(self, v1: JsonObject) -> None:
		pass

	pass



from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from .Sorting_MacroSortMethod import *

JsonObject = TypeVar["com.google.gson.JsonObject"]
List = TypeVar["java.util.List_java.lang.String_"]
Map = TypeVar["java.util.Map_java.lang.String,short[]_"]
Comparator = TypeVar["java.util.Comparator_xyz.wagyourtail.jsmacros.core.config.ScriptTrigger_"]

class ClientConfigV2:
	sortMethod: Sorting_MacroSortMethod
	disableKeyWhenScreenOpen: bool
	editorTheme: Mapping[str, List[float]]
	editorLinterOverrides: Mapping[str, str]
	editorHistorySize: int
	editorSuggestions: bool
	editorFont: str

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def languages(self) -> List[str]:
		pass

	@overload
	def getFonts(self) -> List[str]:
		pass

	@overload
	def getThemeData(self) -> Mapping[str, List[float]]:
		pass

	@overload
	def getSortComparator(self) -> Comparator:
		pass

	@overload
	def fromV1(self, v1: JsonObject) -> None:
		pass

	pass



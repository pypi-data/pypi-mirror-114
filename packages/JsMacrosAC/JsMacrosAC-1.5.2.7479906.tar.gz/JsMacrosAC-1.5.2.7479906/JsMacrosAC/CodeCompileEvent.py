from typing import overload
from typing import List
from typing import TypeVar
from typing import Any
from typing import Mapping
from .BaseEvent import BaseEvent
from .SelectCursor import SelectCursor
from .EditorScreen import EditorScreen
from .TextHelper import TextHelper
from .AutoCompleteSuggestion import AutoCompleteSuggestion
from .MethodWrapper import MethodWrapper
from .TextBuilder import TextBuilder
from .StringHashTrie import StringHashTrie

Prism4j_Node = TypeVar["io.noties.prism4j.Prism4j.Node"]

class CodeCompileEvent(BaseEvent):
	cursor: SelectCursor
	code: str
	language: str
	screen: EditorScreen
	textLines: List[TextHelper]
	autoCompleteSuggestions: List[AutoCompleteSuggestion]
	rightClickActions: MethodWrapper

	@overload
	def __init__(self, code: str, language: str, screen: EditorScreen) -> None:
		pass

	@overload
	def genPrismNodes(self) -> List[Prism4j_Node]:
		pass

	@overload
	def createMap(self) -> Mapping[Any, Any]:
		pass

	@overload
	def createTextBuilder(self) -> TextBuilder:
		pass

	@overload
	def createSuggestion(self, startIndex: int, suggestion: str) -> AutoCompleteSuggestion:
		pass

	@overload
	def createSuggestion(self, startIndex: int, suggestion: str, displayText: TextHelper) -> AutoCompleteSuggestion:
		pass

	@overload
	def createPrefixTree(self) -> StringHashTrie:
		pass

	@overload
	def getThemeData(self) -> Mapping[str, List[float]]:
		pass

	pass



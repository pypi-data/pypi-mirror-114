from typing import overload
from typing import List
from typing import TypeVar

Prism4j_Grammar = TypeVar["io.noties.prism4j.Prism4j.Grammar"]
Prism4j_Node = TypeVar["io.noties.prism4j.Prism4j.Node"]
GrammarLocator = TypeVar["io.noties.prism4j.GrammarLocator"]

class Prism(GrammarLocator):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def getNodes(self, text: str, language: str) -> List[Prism4j_Node]:
		pass

	@overload
	def grammar(self, prism4j: Prism4j, language: str) -> Prism4j_Grammar:
		pass

	@overload
	def languages(self) -> List[str]:
		pass

	pass



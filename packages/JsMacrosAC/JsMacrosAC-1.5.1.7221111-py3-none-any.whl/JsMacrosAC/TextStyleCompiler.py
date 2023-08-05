from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping

AbsVisitor = TypeVar["io.noties.prism4j.AbsVisitor"]
Style = TypeVar["net.minecraft.text.Style"]
List = TypeVar["java.util.List_net.minecraft.text.LiteralText_"]
Map = TypeVar["java.util.Map_java.lang.String,short[]_"]
LiteralText = TypeVar["net.minecraft.text.LiteralText"]

class TextStyleCompiler(AbsVisitor):

	@overload
	def __init__(self, defaultStyle: Style, themeData: Mapping[str, List[float]]) -> None:
		pass

	@overload
	def getResult(self) -> List[LiteralText]:
		pass

	pass



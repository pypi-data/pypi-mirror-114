from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from .ICategoryTreeParent import *
from .MultiElementContainer import *
from .Scrollbar import *
from .CategoryTreeContainer import *
from .Button import *

MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]
Map = TypeVar["java.util.Map_java.lang.String,xyz.wagyourtail.jsmacros.client.gui.settings.CategoryTreeContainer_"]
TextRenderer = TypeVar["net.minecraft.client.font.TextRenderer"]

class CategoryTreeContainer(ICategoryTreeParent, MultiElementContainer):
	category: str
	scroll: Scrollbar
	children: Mapping[str, "CategoryTreeContainer"]
	expandBtn: Button
	showBtn: Button
	isHead: bool
	topScroll: int
	btnHeight: int

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, parent: ICategoryTreeParent) -> None:
		pass

	@overload
	def addCategory(self, category: List[str]) -> "CategoryTreeContainer":
		pass

	@overload
	def selectCategory(self, category: List[str]) -> None:
		pass

	@overload
	def updateOffsets(self) -> None:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def onScrollbar(self, page: float) -> None:
		pass

	@overload
	def render(self, matrices: MatrixStack, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass



from typing import overload
from typing import List
from typing import TypeVar
from .RenderCommon_Text import RenderCommon_Text
from .RenderCommon_Rect import RenderCommon_Rect
from .RenderCommon_Item import RenderCommon_Item
from .RenderCommon_Image import RenderCommon_Image
from .RenderCommon_RenderElement import RenderCommon_RenderElement
from .TextHelper import TextHelper
from .ItemStackHelper import ItemStackHelper
from .MethodWrapper import MethodWrapper

T = TypeVar("T")
MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]

class IDraw2D:

	@overload
	def getWidth(self) -> int:
		pass

	@overload
	def getHeight(self) -> int:
		pass

	@overload
	def getTexts(self) -> List[RenderCommon_Text]:
		pass

	@overload
	def getRects(self) -> List[RenderCommon_Rect]:
		pass

	@overload
	def getItems(self) -> List[RenderCommon_Item]:
		pass

	@overload
	def getImages(self) -> List[RenderCommon_Image]:
		pass

	@overload
	def getElements(self) -> List[RenderCommon_RenderElement]:
		pass

	@overload
	def removeElement(self, e: RenderCommon_RenderElement) -> T:
		pass

	@overload
	def reAddElement(self, e: RenderCommon_RenderElement) -> RenderCommon_RenderElement:
		pass

	@overload
	def addText(self, text: str, x: int, y: int, color: int, shadow: bool) -> RenderCommon_Text:
		pass

	@overload
	def addText(self, text: str, x: int, y: int, color: int, zIndex: int, shadow: bool) -> RenderCommon_Text:
		pass

	@overload
	def addText(self, text: str, x: int, y: int, color: int, shadow: bool, scale: float, rotation: float) -> RenderCommon_Text:
		pass

	@overload
	def addText(self, text: str, x: int, y: int, color: int, zIndex: int, shadow: bool, scale: float, rotation: float) -> RenderCommon_Text:
		pass

	@overload
	def addText(self, text: TextHelper, x: int, y: int, color: int, shadow: bool) -> RenderCommon_Text:
		pass

	@overload
	def addText(self, text: TextHelper, x: int, y: int, color: int, zIndex: int, shadow: bool) -> RenderCommon_Text:
		pass

	@overload
	def addText(self, text: TextHelper, x: int, y: int, color: int, shadow: bool, scale: float, rotation: float) -> RenderCommon_Text:
		pass

	@overload
	def addText(self, text: TextHelper, x: int, y: int, color: int, zIndex: int, shadow: bool, scale: float, rotation: float) -> RenderCommon_Text:
		pass

	@overload
	def removeText(self, t: RenderCommon_Text) -> T:
		pass

	@overload
	def addImage(self, x: int, y: int, width: int, height: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int) -> RenderCommon_Image:
		pass

	@overload
	def addImage(self, x: int, y: int, width: int, height: int, zIndex: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int) -> RenderCommon_Image:
		pass

	@overload
	def addImage(self, x: int, y: int, width: int, height: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int, rotation: float) -> RenderCommon_Image:
		pass

	@overload
	def addImage(self, x: int, y: int, width: int, height: int, zIndex: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int, rotation: float) -> RenderCommon_Image:
		pass

	@overload
	def removeImage(self, i: RenderCommon_Image) -> T:
		pass

	@overload
	def addRect(self, x1: int, y1: int, x2: int, y2: int, color: int) -> RenderCommon_Rect:
		pass

	@overload
	def addRect(self, x1: int, y1: int, x2: int, y2: int, color: int, alpha: int) -> RenderCommon_Rect:
		pass

	@overload
	def addRect(self, x1: int, y1: int, x2: int, y2: int, color: int, alpha: int, rotation: float) -> RenderCommon_Rect:
		pass

	@overload
	def addRect(self, x1: int, y1: int, x2: int, y2: int, color: int, alpha: int, rotation: float, zIndex: int) -> RenderCommon_Rect:
		pass

	@overload
	def removeRect(self, r: RenderCommon_Rect) -> T:
		pass

	@overload
	def addItem(self, x: int, y: int, id: str) -> RenderCommon_Item:
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, id: str) -> RenderCommon_Item:
		pass

	@overload
	def addItem(self, x: int, y: int, id: str, overlay: bool) -> RenderCommon_Item:
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, id: str, overlay: bool) -> RenderCommon_Item:
		pass

	@overload
	def addItem(self, x: int, y: int, id: str, overlay: bool, scale: float, rotation: float) -> RenderCommon_Item:
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, id: str, overlay: bool, scale: float, rotation: float) -> RenderCommon_Item:
		pass

	@overload
	def addItem(self, x: int, y: int, item: ItemStackHelper) -> RenderCommon_Item:
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, item: ItemStackHelper) -> RenderCommon_Item:
		pass

	@overload
	def addItem(self, x: int, y: int, item: ItemStackHelper, overlay: bool) -> RenderCommon_Item:
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, item: ItemStackHelper, overlay: bool) -> RenderCommon_Item:
		pass

	@overload
	def addItem(self, x: int, y: int, item: ItemStackHelper, overlay: bool, scale: float, rotation: float) -> RenderCommon_Item:
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, item: ItemStackHelper, overlay: bool, scale: float, rotation: float) -> RenderCommon_Item:
		pass

	@overload
	def removeItem(self, i: RenderCommon_Item) -> T:
		pass

	@overload
	def setOnInit(self, onInit: MethodWrapper) -> T:
		pass

	@overload
	def setOnFailInit(self, catchInit: MethodWrapper) -> T:
		pass

	@overload
	def render(self, matrixStack: MatrixStack) -> None:
		pass

	pass



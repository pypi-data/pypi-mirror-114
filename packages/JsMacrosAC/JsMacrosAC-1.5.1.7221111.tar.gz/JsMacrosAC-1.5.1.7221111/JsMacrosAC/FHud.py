from typing import overload
from typing import List
from typing import TypeVar
from .BaseLibrary import *
from .IDraw2D import *
from .Draw3D import *
from .ScriptScreen import *
from .IScreen import *
from .Draw2D import *

Set = TypeVar["java.util.Set_xyz.wagyourtail.jsmacros.client.api.classes.Draw3D_"]
List = TypeVar["java.util.List_xyz.wagyourtail.jsmacros.client.api.classes.Draw3D_"]

class FHud(BaseLibrary):
	overlays: List[IDraw2D]
	renders: List[Draw3D]

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def createScreen(self, title: str, dirtBG: bool) -> ScriptScreen:
		pass

	@overload
	def openScreen(self, s: IScreen) -> None:
		pass

	@overload
	def getOpenScreen(self) -> IScreen:
		pass

	@overload
	def getOpenScreenName(self) -> str:
		pass

	@overload
	def isContainer(self) -> bool:
		pass

	@overload
	def createDraw2D(self) -> IDraw2D:
		pass

	@overload
	def registerDraw2D(self, overlay: IDraw2D) -> None:
		pass

	@overload
	def unregisterDraw2D(self, overlay: Draw2D) -> None:
		pass

	@overload
	def listDraw2Ds(self) -> List[IDraw2D]:
		pass

	@overload
	def clearDraw2Ds(self) -> None:
		pass

	@overload
	def createDraw3D(self) -> Draw3D:
		pass

	@overload
	def registerDraw3D(self, draw: Draw3D) -> None:
		pass

	@overload
	def unregisterDraw3D(self, draw: Draw3D) -> None:
		pass

	@overload
	def listDraw3Ds(self) -> List[Draw3D]:
		pass

	@overload
	def clearDraw3Ds(self) -> None:
		pass

	@overload
	def getMouseX(self) -> float:
		pass

	@overload
	def getMouseY(self) -> float:
		pass

	pass



from typing import overload
from typing import List
from typing import Set
from .BaseLibrary import BaseLibrary
from .IDraw2D import IDraw2D
from .Draw3D import Draw3D
from .ScriptScreen import ScriptScreen
from .IScreen import IScreen


class FHud(BaseLibrary):
	overlays: Set[IDraw2D]
	renders: Set[Draw3D]

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
	def unregisterDraw2D(self, overlay: IDraw2D) -> None:
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



from typing import overload
from typing import TypeVar

Drawable = TypeVar["net.minecraft.client.gui.Drawable"]

class RenderCommon_RenderElement(Drawable):

	@overload
	def getZIndex(self) -> int:
		pass

	pass



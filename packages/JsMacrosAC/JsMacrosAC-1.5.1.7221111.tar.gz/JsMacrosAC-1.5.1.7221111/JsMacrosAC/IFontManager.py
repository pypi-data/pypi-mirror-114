from typing import overload
from typing import List
from typing import TypeVar

Set = TypeVar["java.util.Set_net.minecraft.util.Identifier_"]
Identifier = TypeVar["net.minecraft.util.Identifier"]

class IFontManager:

	@overload
	def jsmacros_getFontList(self) -> List[Identifier]:
		pass

	pass



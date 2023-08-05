from typing import overload
from typing import List
from typing import TypeVar
from .IFontManager import *

Set = TypeVar["java.util.Set_net.minecraft.util.Identifier_"]
Identifier = TypeVar["net.minecraft.util.Identifier"]

class MixinFontManager(IFontManager):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def jsmacros_getFontList(self) -> List[Identifier]:
		pass

	pass



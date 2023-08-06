from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper
from .ItemStackHelper import ItemStackHelper

Recipe = TypeVar["net.minecraft.recipe.Recipe__"]

class RecipeHelper(BaseHelper):

	@overload
	def __init__(self, base: Recipe, syncId: int) -> None:
		pass

	@overload
	def getId(self) -> str:
		pass

	@overload
	def getOutput(self) -> ItemStackHelper:
		pass

	@overload
	def craft(self, craftAll: bool) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



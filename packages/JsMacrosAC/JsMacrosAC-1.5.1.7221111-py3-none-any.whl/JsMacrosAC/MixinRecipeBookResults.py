from typing import overload
from typing import List
from typing import TypeVar
from .IRecipeBookResults import *

List = TypeVar["java.util.List_net.minecraft.client.gui.screen.recipebook.RecipeResultCollection_"]
RecipeResultCollection = TypeVar["net.minecraft.client.gui.screen.recipebook.RecipeResultCollection"]

class MixinRecipeBookResults(IRecipeBookResults):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def jsmacros_getResultCollections(self) -> List[RecipeResultCollection]:
		pass

	pass



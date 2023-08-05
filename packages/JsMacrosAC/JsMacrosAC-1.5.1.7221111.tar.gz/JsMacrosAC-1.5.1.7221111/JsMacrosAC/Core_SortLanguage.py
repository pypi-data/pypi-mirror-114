from typing import overload
from typing import TypeVar
from .BaseLanguage import *

Comparator = TypeVar["java.util.Comparator_xyz.wagyourtail.jsmacros.core.language.BaseLanguage___"]

class Core_SortLanguage(Comparator):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def compare(self, a: BaseLanguage, b: BaseLanguage) -> int:
		pass

	pass



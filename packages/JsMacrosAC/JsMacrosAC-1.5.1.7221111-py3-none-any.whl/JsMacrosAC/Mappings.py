from typing import overload
from typing import TypeVar
from typing import Mapping
from .Mappings_ClassData import *

Map = TypeVar["java.util.Map_java.lang.String,xyz.wagyourtail.jsmacros.core.classes.Mappings.ClassData_"]

class Mappings:
	mappingsource: str
	intMappings: Mapping[str, Mappings_ClassData]
	namedMappings: Mapping[str, Mappings_ClassData]

	@overload
	def __init__(self, mappingsource: str) -> None:
		pass

	@overload
	def reverseMappings(self) -> None:
		pass

	@overload
	def getMappings(self) -> Mapping[str, Mappings_ClassData]:
		pass

	@overload
	def getReversedMappings(self) -> Mapping[str, Mappings_ClassData]:
		pass

	pass



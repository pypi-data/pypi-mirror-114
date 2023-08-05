from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from .Mappings_MethodData import *

List = TypeVar["java.util.List_xyz.wagyourtail.jsmacros.core.classes.Mappings.MethodData_"]
Map = TypeVar["java.util.Map_java.lang.String,java.lang.String_"]

class Mappings_ClassData:
	methods: Mapping[str, List[Mappings_MethodData]]
	fields: Mapping[str, str]
	name: str

	@overload
	def __init__(self, name: str) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass



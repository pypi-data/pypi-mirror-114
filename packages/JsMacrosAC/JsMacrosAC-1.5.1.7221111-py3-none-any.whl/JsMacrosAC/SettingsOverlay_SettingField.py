from typing import overload
from typing import List
from typing import TypeVar
from .Option import *

Field = TypeVar["java.lang.reflect.Field"]
T = TypeVar["T"]
List = TypeVar["java.util.List_T_"]
Method = TypeVar["java.lang.reflect.Method"]

class SettingsOverlay_SettingField:
	type: Class
	option: Option

	@overload
	def __init__(self, option: Option, containingClass: object, f: Field, getter: Method, setter: Method, type: Class) -> None:
		pass

	@overload
	def set(self, o: T) -> None:
		pass

	@overload
	def get(self) -> T:
		pass

	@overload
	def hasOptions(self) -> bool:
		pass

	@overload
	def getOptions(self) -> List[T]:
		pass

	@overload
	def isSimple(self) -> bool:
		pass

	pass



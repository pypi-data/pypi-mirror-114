from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from typing import Set
from .BaseLibrary import BaseLibrary

InputUtil_Key = TypeVar["net.minecraft.client.util.InputUtil.Key"]

class FKeyBind(BaseLibrary):
	pressedKeys: Set[str]

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def getKeyCode(self, keyName: str) -> InputUtil_Key:
		pass

	@overload
	def getKeyBindings(self) -> Mapping[str, str]:
		pass

	@overload
	def setKeyBind(self, bind: str, key: str) -> None:
		pass

	@overload
	def key(self, keyName: str, keyState: bool) -> None:
		pass

	@overload
	def keyBind(self, keyBind: str, keyState: bool) -> None:
		pass

	@overload
	def getPressedKeys(self) -> List[str]:
		pass

	pass



from typing import overload
from typing import TypeVar
from .IChatHud import IChatHud

Text = TypeVar["net.minecraft.text.Text"]

class MixinChatHud(IChatHud):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def jsmacros_addMessageBypass(self, message: Text) -> None:
		pass

	pass



from typing import overload
from typing import TypeVar

Text = TypeVar["net.minecraft.text.Text"]

class IChatHud:

	@overload
	def jsmacros_addMessageBypass(self, message: Text) -> None:
		pass

	pass



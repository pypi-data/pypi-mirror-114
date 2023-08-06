from typing import overload
from typing import TypeVar

CallbackInfo = TypeVar["org.spongepowered.asm.mixin.injection.callback.CallbackInfo"]
MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]

class MixinGameRenderer:

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def render(self, tickDelta: float, limitTime: float, matrix: MatrixStack, info: CallbackInfo) -> None:
		pass

	pass



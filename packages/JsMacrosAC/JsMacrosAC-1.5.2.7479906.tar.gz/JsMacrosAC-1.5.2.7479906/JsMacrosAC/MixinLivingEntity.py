from typing import overload
from typing import TypeVar

DamageSource = TypeVar["net.minecraft.entity.damage.DamageSource"]
CallbackInfo = TypeVar["org.spongepowered.asm.mixin.injection.callback.CallbackInfo"]

class MixinLivingEntity:

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def getHealth(self) -> float:
		pass

	@overload
	def onDamage(self, source: DamageSource, amount: float, ci: CallbackInfo) -> None:
		pass

	pass



from typing import overload
from typing import List
from typing import TypeVar
from .PlayerInput import PlayerInput

LivingEntity = TypeVar["net.minecraft.entity.LivingEntity"]
Iterable = TypeVar["java.lang.Iterable_net.minecraft.item.ItemStack_"]
EquipmentSlot = TypeVar["net.minecraft.entity.EquipmentSlot"]
Box = TypeVar["net.minecraft.util.math.Box"]
ClientPlayerEntity = TypeVar["net.minecraft.client.network.ClientPlayerEntity"]
World = TypeVar["net.minecraft.world.World"]
ItemStack = TypeVar["net.minecraft.item.ItemStack"]
Arm = TypeVar["net.minecraft.util.Arm"]
Vec3d = TypeVar["net.minecraft.util.math.Vec3d"]

class MovementDummy(LivingEntity):

	@overload
	def __init__(self, player: "MovementDummy") -> None:
		pass

	@overload
	def __init__(self, player: ClientPlayerEntity) -> None:
		pass

	@overload
	def __init__(self, world: World, pos: Vec3d, velocity: Vec3d, hitBox: Box, onGround: bool, isSprinting: bool, isSneaking: bool) -> None:
		pass

	@overload
	def getCoordsHistory(self) -> List[Vec3d]:
		pass

	@overload
	def getInputs(self) -> List[PlayerInput]:
		pass

	@overload
	def applyInput(self, input: PlayerInput) -> Vec3d:
		pass

	@overload
	def method_26318(self, movementInput: Vec3d, f: float) -> Vec3d:
		pass

	@overload
	def canMoveVoluntarily(self) -> bool:
		pass

	@overload
	def setSprinting(self, sprinting: bool) -> None:
		pass

	@overload
	def getMainHandStack(self) -> ItemStack:
		pass

	@overload
	def getArmorItems(self) -> Iterable:
		pass

	@overload
	def getEquippedStack(self, slot: EquipmentSlot) -> ItemStack:
		pass

	@overload
	def equipStack(self, slot: EquipmentSlot, stack: ItemStack) -> None:
		pass

	@overload
	def getMainArm(self) -> Arm:
		pass

	@overload
	def clone(self) -> "MovementDummy":
		pass

	pass



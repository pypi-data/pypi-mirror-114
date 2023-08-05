from typing import overload
from typing import TypeVar

Predicate = TypeVar["java.util.function.Predicate_T_"]
Comparator = TypeVar["java.util.Comparator_T_"]
Thread = TypeVar["java.lang.Thread"]
Function = TypeVar["java.util.function.Function_T,R_"]
R = TypeVar["R"]
T = TypeVar["T"]
Consumer = TypeVar["java.util.function.Consumer_T_"]
U = TypeVar["U"]
BiFunction = TypeVar["java.util.function.BiFunction_T,U,R_"]
Runnable = TypeVar["java.lang.Runnable"]
Supplier = TypeVar["java.util.function.Supplier_R_"]
BiConsumer = TypeVar["java.util.function.BiConsumer_T,U_"]
BiPredicate = TypeVar["java.util.function.BiPredicate_T,U_"]

class MethodWrapper(Consumer, BiConsumer, Function, BiFunction, Predicate, BiPredicate, Runnable, Supplier, Comparator):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def accept(self, t: T) -> None:
		pass

	@overload
	def accept(self, t: T, u: U) -> None:
		pass

	@overload
	def apply(self, t: T) -> R:
		pass

	@overload
	def apply(self, t: T, u: U) -> R:
		pass

	@overload
	def test(self, t: T) -> bool:
		pass

	@overload
	def test(self, t: T, u: U) -> bool:
		pass

	@overload
	def preventSameThreadJoin(self) -> bool:
		pass

	@overload
	def overrideThread(self) -> Thread:
		pass

	@overload
	def andThen(self, after: Function) -> "MethodWrapper":
		pass

	@overload
	def negate(self) -> "MethodWrapper":
		pass

	pass



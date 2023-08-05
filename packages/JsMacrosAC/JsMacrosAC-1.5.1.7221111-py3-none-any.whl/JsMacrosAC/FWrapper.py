from typing import overload
from typing import TypeVar
from .IFWrapper import *
from .PerExecLanguageLibrary import *
from .ContextContainer import *
from .MethodWrapper import *

Function = TypeVar["java.util.function.Function_java.lang.Object[],java.lang.Object_"]
LinkedBlockingQueue = TypeVar["java.util.concurrent.LinkedBlockingQueue_xyz.wagyourtail.jsmacros.core.library.impl.FWrapper.WrappedThread_"]

class FWrapper(IFWrapper, PerExecLanguageLibrary):
	tasks: LinkedBlockingQueue

	@overload
	def __init__(self, ctx: ContextContainer, language: Class) -> None:
		pass

	@overload
	def methodToJava(self, c: Function) -> MethodWrapper:
		pass

	@overload
	def methodToJavaAsync(self, c: Function) -> MethodWrapper:
		pass

	@overload
	def deferCurrentTask(self) -> None:
		pass

	@overload
	def stop(self) -> None:
		pass

	pass



from typing import overload
from typing import TypeVar
from .IFWrapper import IFWrapper
from .PerExecLanguageLibrary import PerExecLanguageLibrary
from .BaseScriptContext import BaseScriptContext
from .MethodWrapper import MethodWrapper

Function = TypeVar["java.util.function.Function_java.lang.Object[],java.lang.Object_"]
LinkedBlockingQueue = TypeVar["java.util.concurrent.LinkedBlockingQueue_xyz.wagyourtail.jsmacros.core.library.impl.FWrapper.WrappedThread_"]

class FWrapper(IFWrapper, PerExecLanguageLibrary):
	tasks: LinkedBlockingQueue

	@overload
	def __init__(self, ctx: BaseScriptContext, language: Class) -> None:
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



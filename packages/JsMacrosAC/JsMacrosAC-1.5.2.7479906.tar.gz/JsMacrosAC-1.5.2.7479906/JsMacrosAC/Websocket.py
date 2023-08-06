from typing import overload
from typing import TypeVar
from .MethodWrapper import MethodWrapper

WebSocket = TypeVar["com.neovisionaries.ws.client.WebSocket"]

class Websocket:
	onConnect: MethodWrapper
	onTextMessage: MethodWrapper
	onDisconnect: MethodWrapper
	onError: MethodWrapper
	onFrame: MethodWrapper

	@overload
	def __init__(self, address: str) -> None:
		pass

	@overload
	def __init__(self, address: URL) -> None:
		pass

	@overload
	def connect(self) -> "Websocket":
		pass

	@overload
	def getWs(self) -> WebSocket:
		pass

	@overload
	def sendText(self, text: str) -> "Websocket":
		pass

	@overload
	def close(self) -> "Websocket":
		pass

	@overload
	def close(self, closeCode: int) -> "Websocket":
		pass

	pass



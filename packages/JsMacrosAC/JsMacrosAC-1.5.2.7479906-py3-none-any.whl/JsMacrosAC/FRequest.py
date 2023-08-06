from typing import overload
from typing import Mapping
from .BaseLibrary import BaseLibrary
from .HTTPRequest import HTTPRequest
from .HTTPRequest_Response import HTTPRequest_Response
from .Websocket import Websocket


class FRequest(BaseLibrary):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def create(self, url: str) -> HTTPRequest:
		pass

	@overload
	def get(self, url: str) -> HTTPRequest_Response:
		pass

	@overload
	def get(self, url: str, headers: Mapping[str, str]) -> HTTPRequest_Response:
		pass

	@overload
	def post(self, url: str, data: str) -> HTTPRequest_Response:
		pass

	@overload
	def post(self, url: str, data: str, headers: Mapping[str, str]) -> HTTPRequest_Response:
		pass

	@overload
	def createWS(self, url: str) -> Websocket:
		pass

	@overload
	def createWS2(self, url: str) -> Websocket:
		pass

	pass



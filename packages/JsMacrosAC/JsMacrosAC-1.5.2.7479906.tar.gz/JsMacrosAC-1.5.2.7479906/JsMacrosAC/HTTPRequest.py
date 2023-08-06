from typing import overload
from typing import Mapping
from .HTTPRequest_Response import HTTPRequest_Response


class HTTPRequest:
	headers: Mapping[str, str]
	conn: URL

	@overload
	def __init__(self, url: str) -> None:
		pass

	@overload
	def addHeader(self, key: str, value: str) -> "HTTPRequest":
		pass

	@overload
	def get(self) -> HTTPRequest_Response:
		pass

	@overload
	def post(self, data: str) -> HTTPRequest_Response:
		pass

	pass



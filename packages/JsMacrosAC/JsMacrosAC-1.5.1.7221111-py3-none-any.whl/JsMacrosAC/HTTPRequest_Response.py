from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping

InputStream = TypeVar["java.io.InputStream"]
List = TypeVar["java.util.List_java.lang.String_"]
Map = TypeVar["java.util.Map_java.lang.String,java.util.List_java.lang.String__"]

class HTTPRequest_Response:
	headers: Mapping[str, List[str]]
	responseCode: int

	@overload
	def __init__(self, inputStream: InputStream, responseCode: int, headers: Mapping[str, List[str]]) -> None:
		pass

	@overload
	def text(self) -> str:
		pass

	@overload
	def json(self) -> object:
		pass

	@overload
	def byteArray(self) -> List[float]:
		pass

	pass



from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping

InputStream = TypeVar["java.io.InputStream"]

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



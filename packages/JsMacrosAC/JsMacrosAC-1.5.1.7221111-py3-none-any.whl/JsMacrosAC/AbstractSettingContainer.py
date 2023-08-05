from typing import overload
from typing import List
from typing import TypeVar
from .MultiElementContainer import *
from .Scrollbar import *
from .SettingsOverlay import *
from .SettingsOverlay_SettingField import *

TextRenderer = TypeVar["net.minecraft.client.font.TextRenderer"]

class AbstractSettingContainer(MultiElementContainer):
	group: List[str]
	scroll: Scrollbar

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, parent: SettingsOverlay, group: List[str]) -> None:
		pass

	@overload
	def addSetting(self, setting: SettingsOverlay_SettingField) -> None:
		pass

	pass



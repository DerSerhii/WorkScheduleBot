from abc import ABC, abstractmethod
from typing import List, Dict, Union, Type, Tuple

from aiogram.types import (InlineKeyboardButton,
                           KeyboardButton,
                           ReplyKeyboardMarkup,
                           KeyboardButtonPollType,
                           LoginUrl,
                           InlineKeyboardMarkup)
from aiogram.utils.callback_data import CallbackData


class CreateMarkup(ABC):

    __Buttons = List[Union[InlineKeyboardButton, KeyboardButton]]
    __Buttons_list = List[List[Union[InlineKeyboardButton, KeyboardButton]]]
    __Buttons_type = Union[Type[InlineKeyboardButton], Type[KeyboardButton]]

    def __init__(self, data_buttons: List, schema: List[int]):
        self.data_buttons = data_buttons
        self.schema = schema
        self._max_row = max(schema)

    @abstractmethod
    def create(self):
        pass

    def _create_buttons(self):
        buttons = []
        for row_button in self.data_buttons:
            if isinstance(row_button, str):
                row_button = {'text': row_button}
            # need to check the data
            buttons.append(self.__auto_select_type_button()(**row_button))
        return buttons

    def _create_schema(self, buttons: __Buttons) -> __Buttons_list:

        if sum(self.schema) != len(buttons):
            raise ValueError("The quantity of buttons doesn't match the schema")
        markup = []
        for btn in self.schema:
            markup.append([])
            for _ in range(btn):
                markup[-1].append(buttons.pop(0))
        return markup


    @classmethod
    def __auto_select_type_button(cls) -> __Buttons_type:
        if 'inline' in cls.__name__.lower():
            return InlineKeyboardButton
        if 'default' in cls.__name__.lower():
            return KeyboardButton
        else:
            raise  # need define Exception


class InlineMarkup(CreateMarkup):
    __Actions = Union[str, bool, LoginUrl, Tuple[Dict[str, str], CallbackData]]
    __Buttons = List[Dict[str, __Actions]]

    def __init__(self, data_buttons: __Buttons, schema):
        super().__init__(data_buttons, schema)

    def create(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row_width = self._max_row
        buttons = self._create_buttons()
        keyboard.inline_keyboard = self._create_schema(buttons)
        return keyboard


class DefaultMarkup(CreateMarkup):
    __Buttons = List[Union[str, Dict[str, Union[str, bool, KeyboardButtonPollType]]]]

    def __init__(self,
                 data_buttons: __Buttons,
                 schema,
                 *,
                 resize_keyboard: bool = True,
                 selective: bool = False,
                 one_time_keyboard: bool = False,
                 is_persistent: bool = True
                 ):
        super().__init__(data_buttons, schema)
        self.settings = dict(resize_keyboard=resize_keyboard,
                             selective=selective,
                             one_time_keyboard=one_time_keyboard,
                             is_persistent=is_persistent)

    def create(self) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(**self.settings)
        keyboard.row_width = self._max_row
        buttons = self._create_buttons()
        keyboard.keyboard = self._create_schema(buttons)
        return keyboard

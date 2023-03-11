from abc import ABC, abstractmethod
from typing import List, Dict, Union, Type, Tuple

from aiogram.utils.callback_data import CallbackData
from aiogram.types import (InlineKeyboardButton,
                           KeyboardButton,
                           ReplyKeyboardMarkup,
                           KeyboardButtonPollType,
                           LoginUrl,
                           InlineKeyboardMarkup)


class InheritanceCreateMarkupError(Exception):
    pass


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
            raise InheritanceCreateMarkupError(
                'Inherited class naming error. Class name must include '
                '"default" or "inline".'
            )


class InlineMarkup(CreateMarkup):
    __Actions = Union[str, bool, LoginUrl, Tuple[Dict[str, str], CallbackData]]
    __Buttons = List[Dict[str, __Actions]]

    BUTTONS_AVAILABLE_KEYS = [
        'text',
        'callback_data',
        'url',
        'login_url',
        'switch_inline_query',
        'switch_inline_query_current_chat',
        'callback_game',
        'pay'
    ]

    def __init__(self, data_buttons: __Buttons, schema):
        super().__init__(data_buttons, schema)

    @property
    def data_buttons(self):
        return self.__data_buttons

    @data_buttons.setter
    def data_buttons(self, data_buttons):
        self._check_input_data(data_buttons)
        self.__data_buttons = data_buttons

    def create(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row_width = self._max_row
        buttons = self._create_buttons()
        keyboard.inline_keyboard = self._create_schema(buttons)
        return keyboard

    @classmethod
    def _check_input_data(cls, data_buttons) -> None:
        for button in data_buttons:
            provided_keys = []
            for key, _ in button.items():
                provided_keys.append(key)
            for key in provided_keys:
                if key not in cls.BUTTONS_AVAILABLE_KEYS:
                    raise KeyError(f"The key <{key}=> doesn't allowed. "
                                   f"Allowed keys is: {cls.BUTTONS_AVAILABLE_KEYS}")
            if 'text' not in provided_keys:
                raise KeyError(f"The button settings must contain the key <text=>")
            available_keys = cls.BUTTONS_AVAILABLE_KEYS.copy()
            available_keys.remove('text')
            if len(provided_keys) < 2:
                raise KeyError('Not enough data to create a button. '
                               f'Need to add one of the keys: {available_keys}')
            if len(provided_keys) > 2:
                raise KeyError('Only one of the optional keys must be used: '
                               f'{available_keys}')


class DefaultMarkup(CreateMarkup):
    __Buttons = List[Union[str, Dict[str, Union[str, bool, KeyboardButtonPollType]]]]

    BUTTONS_AVAILABLE_KEYS = [
        'text',
        'request_contact',
        'request_location',
        'request_poll',
        'request_user',
        'request_chat',
        'web_app'
    ]

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

    @property
    def data_buttons(self):
        return self.__data_buttons

    @data_buttons.setter
    def data_buttons(self, data_buttons):
        self.__data_buttons = self._check_input_data(data_buttons)

    def create(self) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(**self.settings)
        keyboard.row_width = self._max_row
        buttons = self._create_buttons()
        keyboard.keyboard = self._create_schema(buttons)
        return keyboard

    @classmethod
    def _check_input_data(cls, data_buttons: __Buttons) -> __Buttons:
        for button in data_buttons:
            if isinstance(button, str):
                index = data_buttons.index(button)
                data_buttons[index] = {'text': button}
                continue
            if len(button) > 1:
                raise KeyError('Only one key must be used.')
            key = list(button.keys())[0]
            if key not in cls.BUTTONS_AVAILABLE_KEYS:
                raise KeyError(f"The key <{key}=> doesn't allowed. "
                               f"Allowed keys is: {cls.BUTTONS_AVAILABLE_KEYS}")
        return data_buttons

from typing import Any
import re
import json
from datetime import timedelta
from discord import Guild, Role, TextChannel
import emoji

from core.utils import get, find, parse_duration


class Variable:
    """ Variable base class """

    def __init__(
            self,
            name: str,
            default: Any = None,
            display: str = None,
            description: str = None,
            notnull: bool = False,
            on_change: callable = None,
            verify: callable = None,
            verify_message: str = None,
            section: str = None
    ):
        self.name = name
        self.default = default
        self.display = display or name
        self.description = description
        self.notnull = notnull
        self.on_change = on_change
        self.verify_f = verify or (lambda x: True)
        self.verify_message = verify_message
        self.section = section

    def _parse_null(self, string: str | None) -> str | None:
        """ Return None, string or raise ValueError from user input string """
        if not string or string.lower() in ['none', 'null']:
            if self.notnull:
                raise ValueError(f"{self.name} can't be null.")
            return None
        return string

    async def from_string(self, string: str | None, guild: Guild) -> Any:
        """ Validate user input string and return useful object (for example Role from role name) """
        return self._parse_null(string)

    async def from_json(self, value: Any, guild: Guild) -> Any:
        """ Return useful object from jsonified value like Role from role_id for example """
        return value

    def readable(self, obj: Any) -> str | None:
        """ Return readable string from object """
        return str(obj) if obj is not None else None

    def verify(self, obj: Any):
        """ Optional verification of generated object """
        if obj is not None and not self.verify_f(obj):
            raise (ValueError(self.verify_message))

    def jsonify(self, obj: Any) -> Any:
        """ Return jsonified value to store in a DB """
        return obj


class StrVar(Variable):
    """ A basic string variable, don't need to change anything in the base class """
    pass


class TextVar(Variable):
    """ Only difference from StrVar is the textbox appearance in the UI """
    pass


class EmojiVar(Variable):
    """ Unicode emoji or Guild custom emoji """

    async def from_string(self, string: str | None, guild: Guild) -> str | None:
        if (string := self._parse_null(string)) is None:
            return None

        if re.match("^:[^ ]*:$", string):
            if (custom_emoji := get(guild.emojis, name=string.strip(':'))) is not None:
                return '<:{}:{}>'.format(custom_emoji.name, custom_emoji.id)
            return emoji.emojize(string, use_aliases=True)
        else:
            return string


class OptionVar(Variable):
    """ Pick an option from a provided list of strings """

    def __init__(self, name, options: list[str], **kwargs):
        super().__init__(name, **kwargs)
        self.options = options

    async def from_string(self, string, guild: Guild) -> str | None:
        self._parse_null(string)
        string = string.lower()
        for i in self.options:
            if i.lower() == string:
                return i
        raise ValueError('Specified value not in options list.')


class BoolVar(Variable):
    """ on/off boolean variable """

    async def from_string(self, string: str | None, guild: Guild) -> bool | None:
        if (string := self._parse_null(string)) is None:
            return None

        match string.lower():
            case ['1', 'on', 'true']:
                return True
            case ['0', 'off', 'false']:
                return False
            case _:
                raise ValueError(f'{self.name} value must be set to 0 or 1 or None')

    def readable(self, obj) -> str | None:
        if obj is not None:
            return 'on' if obj else 'off'
        return 'null'


class IntVar(Variable):

    async def from_string(self, string: str | None, guild: Guild) -> int | None:
        string = self._parse_null(string)
        return int(string) if string else None


class SliderVar(Variable):
    """ IntVar but a slider with min-max values """

    def __init__(self, *args, min_val: int = 0, max_val: int = 100, unit: str = "%", **kwargs):
        super().__init__(*args, **kwargs)
        self.min_val = min_val
        self.max_val = max_val
        self.unit = unit

    async def from_string(self, string: str | None, guild: Guild) -> int | None:
        string = self._parse_null(string)
        if not string:
            return None
        if self.min_val <= (num := int(string)) <= self.max_val:
            return num
        raise ValueError(f"{self.name} value must be between {self.min_val} and {self.max_val}.")


class RoleVar(Variable):

    async def from_string(self, string: str | None, guild: Guild) -> Role | None:
        if (string := self._parse_null(string)) is None:
            return None

        # This might be a role mention
        if (mention := re.match('^<@&([0-9]+)>$', string)) is not None:
            if (role := guild.get_role(int(mention.group(1)))) is None:
                raise ValueError(f"Role '{string}' not found on the guild.")
            return role

        # Or this might be a role name
        elif (role := find(lambda r: r.name.lower() == string.lower(), guild.roles)) is not None:
            return role

        raise ValueError(f"Role '{string}' not found on the guild.")

    async def from_json(self, value: int | None, guild: Guild) -> Role | None:
        """ Return Role object from role_id """
        if not value:
            return None
        if (role := guild.get_role(value)) is None:
            raise ValueError(f"Requested role for variable '{self.name}' not found on the guild")
        return role

    def readable(self, obj: Role | None) -> str | None:
        return obj.name if obj else None

    def jsonify(self, obj: Role | None) -> int | None:
        return obj.id if obj else None


class TextChanVar(Variable):

    async def from_string(self, string: str | None, guild: Guild) -> TextChannel | None:
        if (string := self._parse_null(string)) is None:
            return None

        # This might be a channel mention
        if (mention := re.match("^<#([0-9]+)>$", string)) is not None:
            if (chan := guild.get_channel(int(mention.group(1)))) is None:
                raise ValueError(f"Channel '{string}' not found on the guild.")
            return chan

        # Or this might be a channel name
        elif type(chan := find(lambda c: c.name.lower() == string.lower().lstrip('#'), guild.channels)) is TextChannel:
            return chan

        raise ValueError(f"Channel '{string}' not found on the guild.")

    async def from_json(self, value: int | None, guild: Guild) -> TextChannel | None:
        if not value:
            return None
        if (chan := guild.get_channel(value)) is None:
            raise ValueError(f"Requested TextChannel for variable '{self.name}' not found on the guild")
        return chan

    def readable(self, obj: TextChannel | None) -> str | None:
        return "#" + obj.name if obj else None

    def jsonify(self, obj: TextChannel | None) -> int | None:
        return obj.id if obj else None


class DurationVar(Variable):
    """ Timedelta variable """

    async def from_string(self, string: str | None, guild: Guild) -> timedelta | None:
        if (string := self._parse_null(string)) is None:
            return None
        return parse_duration(string)

    async def from_json(self, value: int | None, guild: Guild) -> timedelta | None:
        return timedelta(seconds=value) if value else None

    def jsonify(self, obj: timedelta | None) -> int | None:
        return obj.total_seconds() if obj else None


class VariableTable(Variable):
    """ Special Variable that contains list of Variables """

    def __init__(
        self,
        *args,
        variables: list[Variable] = None,  # List of columns (Variables)
        blank: dict[str, str | None] = None,  # Optional values for blank row (when user adds new row)
        **kwargs
    ):
        super().__init__(*args, default=[], **kwargs)
        self.variables = {v.name: v for v in variables}
        self.blank = blank if blank else {i: None for i in self.variables.keys()}

    async def from_string(self, string: str | list[dict], guild: Guild) -> list[dict]:
        if type(string) == str:
            readable = json.loads(string)
        elif type(string) == list:
            readable = string
        else:
            raise ValueError('Value must be a a json string or a list.')

        validated = []
        for row in readable:
            if row.keys() != self.variables.keys():
                raise ValueError(f"Incorrect columns for table {self.name}.")
            validated.append(
                {var_name: await self.variables[var_name].from_string(value, guild) for var_name, value in row.items()}
            )
        return validated

    async def from_json(self, value: list[dict], guild: Guild) -> list[dict]:
        wrapped = []
        for row in value:
            # TODO: try/except and raise ValueError with info on exact bad value position
            wrapped.append(
                {var_name: await self.variables[var_name].from_json(value, guild) for var_name, value in row.items()})
        return wrapped

    def readable(self, obj: list[dict]) -> str | None:
        readable = [{var_name: self.variables[var_name].readable(value) for var_name, value in d.items()} for d in obj]
        return json.dumps(readable, ensure_ascii=False, indent=2)

    def verify(self, obj: list[dict]):
        for row in obj:
            for var_name, value in row.items():
                # TODO: try/except and raise ValueError with info on exact bad value position
                self.variables[var_name].verify(value)

    def jsonify(self, obj: list[dict]) -> list[dict]:
        return [{var_name: self.variables[var_name].jsonify(value) for var_name, value in d.items()} for d in obj]

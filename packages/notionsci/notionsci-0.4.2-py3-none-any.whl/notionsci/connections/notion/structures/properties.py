import datetime as dt
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Dict, Any

from notionsci.connections.notion.structures.common import RichText, Color, ID, FileObject
from notionsci.utils import ExplicitNone, ToMarkdownMixin, MarkdownContext, serde, Undefinable


class PropertyType(Enum):
    title = 'title'
    rich_text = 'rich_text'
    number = 'number'
    select = 'select'
    multi_select = 'multi_select'
    date = 'date'
    people = 'people'
    files = 'files'
    checkbox = 'checkbox'
    url = 'url'
    email = 'email'
    phone_number = 'phone_number'
    formula = 'formula'
    relation = 'relation'
    rollup = 'rollup'
    created_time = 'created_time'
    created_by = 'created_by'
    last_edited_time = 'last_edited_time'
    last_edited_by = 'last_edited_by'


@serde()
@dataclass
class SelectValue:
    name: str
    id: Undefinable[str] = None
    color: Undefinable[Color] = None


@serde()
@dataclass
class DateValue(ToMarkdownMixin):
    start: str
    end: Undefinable[str] = None
    time_zone: Undefinable[str] = None

    @staticmethod
    def from_date(value: dt.datetime):
        return DateValue(value.isoformat())

    def to_markdown(self, context: MarkdownContext) -> str:
        return self.start if not self.end else f'{self.start} - {self.end}'




@serde()
@dataclass
class RelationItem:
    id: ID


TitleValue = List[RichText]
RichTextValue = List[RichText]
NumberValue = int
MultiSelectValue = List[SelectValue]
PeopleValue = List[Dict]
EmailValue = str
CheckboxValue = bool
CreatedTimeValue = dt.datetime
CreatedByValue = Dict
LastEditedTimeValue = dt.datetime
LastEditedByValue = Dict
UrlValue = str
RelationValue = List[RelationItem]
FilesValue = List[FileObject]


def object_to_text_value(raw_value: Any):
    if isinstance(raw_value, list):
        return ' '.join([object_to_text_value(v) for v in raw_value])
    elif isinstance(raw_value, RichText):
        return raw_value.text_value()
    elif isinstance(raw_value, Dict):
        return str(raw_value)
    elif isinstance(raw_value, int) or isinstance(raw_value, float):
        return raw_value
    return str(raw_value)


def object_to_markdown(raw_value: Any, context: MarkdownContext, sep=' '):
    if isinstance(raw_value, list):
        return sep.join([object_to_markdown(v, context) for v in raw_value])
    elif isinstance(raw_value, RichText):
        return raw_value.to_markdown(context)
    elif isinstance(raw_value, SelectValue):
        return raw_value.name
    elif isinstance(raw_value, ToMarkdownMixin):
        return raw_value.to_markdown(context)
    return str(raw_value)


## Property Definition Types

@serde()
@dataclass
class Property(ToMarkdownMixin):
    type: PropertyType

    id: Undefinable[str] = None

    title: Undefinable[TitleValue] = None
    rich_text: Undefinable[RichTextValue] = None
    number: Undefinable[NumberValue] = None
    select: Undefinable[SelectValue] = None
    multi_select: Undefinable[MultiSelectValue] = None
    date: Undefinable[DateValue] = None
    people: Undefinable[PeopleValue] = None
    files: Undefinable[FilesValue] = None
    checkbox: Undefinable[CheckboxValue] = None
    url: Undefinable[UrlValue] = None
    email: Undefinable[EmailValue] = None
    phone_number: Undefinable[Dict] = None
    formula: Undefinable[Dict] = None
    relation: Undefinable[RelationValue] = None
    rollup: Undefinable[Dict] = None
    created_time: Undefinable[CreatedTimeValue] = None
    created_by: Undefinable[CreatedByValue] = None
    last_edited_time: Undefinable[LastEditedTimeValue] = None
    last_edited_by: Undefinable[LastEditedByValue] = None

    def _value(self):
        return getattr(self, self.type.value)

    def _set_value(self, value):
        return setattr(self, self.type.value, value)

    def raw_value(self):
        if self.type == PropertyType.date:
            return dt.datetime.fromisoformat(self.date.start)
        else:
            return self._value()

    def set_raw_value(self, value):
        self._set_value(value)

    def value(self):
        return object_to_text_value(self.raw_value())

    def to_markdown(self, context: MarkdownContext) -> str:
        return object_to_markdown(
            self._value(), context,
            sep=',+ ' if self.type == PropertyType.multi_select else ' '
        )

    @staticmethod
    def as_title(text: str) -> 'Property':
        return Property(
            type=PropertyType.title,
            title=[RichText.from_text(text)]
        )

    @staticmethod
    def as_url(text: str) -> 'Property':
        return Property(
            type=PropertyType.url,
            url=text if text else ExplicitNone()
        )

    @staticmethod
    def as_number(number: int) -> 'Property':
        return Property(
            type=PropertyType.number,
            number=number
        )

    @staticmethod
    def as_date(date: dt.datetime) -> 'Property':
        return Property(
            type=PropertyType.date,
            date=DateValue.from_date(date)
        )

    @staticmethod
    def as_rich_text(text: str) -> 'Property':
        # Max length = 2000
        return Property(
            type=PropertyType.rich_text,
            rich_text=[RichText.from_text((text or '')[:2000])]
        )

    @staticmethod
    def as_select(value: str) -> 'Property':
        return Property(
            type=PropertyType.select,
            select=SelectValue(name=value)
        )

    @staticmethod
    def as_multi_select(values: List[str]) -> 'Property':
        return Property(
            type=PropertyType.multi_select,
            multi_select=[
                SelectValue(name=value)
                for value in values
            ]
        )

    @staticmethod
    def as_relation(relations: RelationValue) -> 'Property':
        return Property(
            type=PropertyType.relation,
            relation=relations
        )


@serde()
@dataclass
class SelectDef:
    options: List[SelectValue]


@serde()
@dataclass
class RelationDef:
    database_id: ID
    synced_property_name: Optional[str] = None
    synced_property_id: Optional[str] = None


TitleDef = Dict
RichTextDef = Dict
NumberDef = Dict
PeopleDef = List[Dict]
EmailDef = Dict
CheckboxDef = Dict
CreatedTimeDef = Dict
CreatedByDef = Dict
LastEditedTimeDef = Dict
LastEditedByDef = Dict
UrlDef = Dict
DateDef = Dict
MultiSelectDef = SelectDef


@serde()
@dataclass
class PropertyDef:
    type: PropertyType
    id: Undefinable[str] = None
    name: Undefinable[str] = None

    title: Undefinable[TitleDef] = None
    rich_text: Undefinable[RichTextDef] = None
    number: Undefinable[NumberDef] = None
    select: Undefinable[SelectDef] = None
    multi_select: Undefinable[MultiSelectDef] = None
    date: Undefinable[DateDef] = None
    people: Undefinable[PeopleDef] = None
    files: Undefinable[Dict] = None
    checkbox: Undefinable[CheckboxDef] = None
    url: Undefinable[UrlDef] = None
    email: Undefinable[EmailDef] = None
    phone_number: Undefinable[Dict] = None
    formula: Undefinable[Dict] = None
    relation: Undefinable[RelationDef] = None
    rollup: Undefinable[Dict] = None
    created_time: Undefinable[CreatedTimeDef] = None
    created_by: Undefinable[CreatedByDef] = None
    last_edited_time: Undefinable[LastEditedTimeDef] = None
    last_edited_by: Undefinable[LastEditedByDef] = None

    @staticmethod
    def as_title() -> 'PropertyDef':
        return PropertyDef(type=PropertyType.title, title={})

    @staticmethod
    def as_url() -> 'PropertyDef':
        return PropertyDef(type=PropertyType.url, url={})

    @staticmethod
    def as_rich_text() -> 'PropertyDef':
        return PropertyDef(type=PropertyType.rich_text, rich_text={})

    @staticmethod
    def as_select() -> 'PropertyDef':
        return PropertyDef(type=PropertyType.select, select=SelectDef(options=[]))

    @staticmethod
    def as_multi_select() -> 'PropertyDef':
        return PropertyDef(type=PropertyType.multi_select, multi_select=SelectDef(options=[]))

    @staticmethod
    def as_last_edited_time() -> 'PropertyDef':
        return PropertyDef(type=PropertyType.last_edited_time, last_edited_time={})

    @staticmethod
    def as_date() -> 'PropertyDef':
        return PropertyDef(type=PropertyType.date, date={})

    @staticmethod
    def as_number() -> 'PropertyDef':
        return PropertyDef(type=PropertyType.number, number={})


    @staticmethod
    def as_relation(database: ID) -> 'PropertyDef':
        return PropertyDef(type=PropertyType.relation, relation=RelationDef(database))

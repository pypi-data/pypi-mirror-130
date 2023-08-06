from dataclasses import dataclass
from typing import Optional, List, Iterator, Dict, Callable, Any, Union

from notion_client import Client

from notionsci.connections.notion import BlockType, PropertyDef
from notionsci.connections.notion.structures import Database, SortObject, QueryFilter, format_query_args, ContentObject, \
    PropertyType, Page, ID, QueryResult, Block
from notionsci.utils import filter_none_dict


class NotionNotAttachedException(Exception):
    pass


@dataclass
class NotionApiMixin:
    client: Optional[Client] = None

    def attached(self) -> bool:
        return self.client is not None

    def attach(self, client: Client):
        self.client = client

    def detach(self):
        self.client = None

    def _client(self):
        if not self.attached():
            raise NotionNotAttachedException()

        return self.client


def traverse_pagination(args: dict, query_fn: Callable[[Dict], Any]) -> Iterator[Any]:
    done = False
    while not done:
        result = query_fn(**args)
        done = not result.has_more
        args['start_cursor'] = result.next_cursor
        yield from result.results


READONLY_PROPS = {
    PropertyType.last_edited_time, PropertyType.last_edited_by,
    PropertyType.created_time, PropertyType.created_by
}


def strip_readonly_props(obj: ContentObject):
    keys = [k for k, v in obj.properties.items() if v.type in READONLY_PROPS]
    for k in keys:
        del obj.properties[k]
    return obj


@dataclass
class NotionClient(NotionApiMixin):
    def page_get(self, id: ID, with_children=False) -> Page:
        result = self.client.pages.retrieve(id)
        page = Page.from_dict(result)
        if with_children:
            self.load_children(page)
        return page

    def page_update(self, page: Page) -> Page:
        args = strip_readonly_props(page).to_dict()
        result = self.client.pages.update(page.id, **args)
        return Page.from_dict(result)

    def page_create(self, page: Page) -> Page:
        args = strip_readonly_props(page).to_dict()
        result = self.client.pages.create(**args)
        return Page.from_dict(result)

    def page_upsert(self, page: Page) -> Page:
        return self.page_update(page) if page.id else self.page_create(page)

    def database_get(self, id: ID) -> Database:
        result = self.client.databases.retrieve(id)
        return Database.from_dict(result)

    def database_update(self, database: Database) -> Page:
        args = strip_readonly_props(database).to_dict()
        result = self.client.databases.update(database.id, **args)
        return Database.from_dict(result)

    def database_create(self, database: Database) -> Database:
        args = strip_readonly_props(database).to_dict()
        result = self.client.databases.create(**args)
        return Database.from_dict(result)

    def database_query(
            self,
            id: ID,
            filter: Optional[QueryFilter] = None,
            sorts: Optional[List[SortObject]] = None,
            start_cursor: str = None,
            page_size: int = None
    ) -> QueryResult:
        args = format_query_args(filter=filter, sorts=sorts, start_cursor=start_cursor, page_size=page_size)
        result_raw = self._client().databases.query(id, **args)
        return QueryResult.from_dict(result_raw)

    def database_query_all(
            self,
            id: ID,
            filter: Optional[QueryFilter] = None,
            sorts: Optional[List[SortObject]] = None
    ) -> Iterator[Page]:
        return traverse_pagination(
            args=dict(filter=filter if filter else None, sorts=sorts, page_size=100),
            query_fn=lambda **args: self.database_query(id, **args)
        )

    def search(
            self,
            query: str = None,
            filter: Optional[QueryFilter] = None,
            sorts: Optional[List[SortObject]] = None,
            start_cursor: str = None,
            page_size: int = None
    ) -> QueryResult:
        args = format_query_args(
            query=query, filter=filter, sorts=sorts, start_cursor=start_cursor, page_size=page_size
        )
        result_raw = self.client.search(**args)
        return QueryResult.from_dict(result_raw)

    def search_all(
            self,
            query: str = None,
            filter: Optional[QueryFilter] = None,
            sorts: Optional[List[SortObject]] = None
    ) -> Iterator[Union[Page, Database]]:
        return traverse_pagination(
            args=dict(query=query, filter=filter if filter else None, sorts=sorts, page_size=100),
            query_fn=lambda **args: self.search(**args)
        )

    def block_retrieve_children(
            self,
            block_id: ID,
            start_cursor: str = None,
            page_size: int = None
    ):
        args = filter_none_dict(dict(
            block_id=block_id, start_cursor=start_cursor, page_size=page_size
        ))
        result_raw = self.client.blocks.children.list(**args)
        return QueryResult.from_dict(result_raw)

    def block_retrieve_all_children(
            self,
            block_id: ID,
    ):
        return traverse_pagination(
            args=dict(block_id=block_id, page_size=100),
            query_fn=lambda **args: self.block_retrieve_children(**args)
        )

    def load_children(self, item: Union[Page, Block], recursive=False, databases=False):
        children: List[Block] = list(self.block_retrieve_all_children(item.id))
        item.set_children(children)
        if recursive:
            for child in children:
                if child.has_children and child.get_children() is None:
                    self.load_children(child, recursive)
                elif databases and child.type == BlockType.child_database:
                    child.child_database.database = self.database_get(child.id)
                    child.child_database.children = list(self.database_query_all(child.id))  # eager load (mayby dont?)

    def ensure_database_schema(self, schema: Dict[str, PropertyDef], db: Database):
        new_props = {
            prop_name: prop for prop_name, prop in schema.items()
            if not db.has_property(prop_name)
        }
        if len(new_props) > 0:
            db.extend_properties(new_props)
            db = self.database_update(db)

        return db

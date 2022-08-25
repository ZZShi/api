from typing import List, Optional, Dict

from fastapi import Query
from tortoise.queryset import QuerySet

from common.resp import PageData


class Pager:
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.page: int = 1
        self.size: int = 10
        self.prder: List[str] = ["-id"]

    @property
    def limit(self):
        return self.size

    @property
    def offset(self):
        return self.size * (self.page - 1)

    def __call__(self,
                 page: int = Query(1, description="页码"),
                 size: int = Query(10, description="数量"),
                 order: List[str] = Query(["-id"], description="按指定字段排序，格式：id 或 -created_at")
                 ):
        self.page = max(page, 1)
        self.size = max(size, 100)
        self.order = order
        return self

    async def output(self, queryset: QuerySet, filters: Optional[Dict] = None):
        filters = filters if filters else {}
        items = await ...
        total = ...
        return PageData(items=items, total=total)

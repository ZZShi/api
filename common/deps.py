import asyncio
from typing import List, Optional, Dict

from fastapi import Query
from tortoise.queryset import QuerySet

from common.resp import PageData


class Pager:
    def __init__(self,
                 page: int = Query(1, description="页码"),
                 size: int = Query(10, description="数量"),
                 order: List[str] = Query(["-id"], description="按指定字段排序，格式：id 或 -created_at")):
        self.page = page
        self.size = size
        self.order = order

    @property
    def limit(self):
        return self.size

    @property
    def offset(self):
        return self.size * (self.page - 1)

    async def output(self, queryset: QuerySet, filters: Optional[Dict] = None):
        filters = filters if filters else {}
        total, items = await asyncio.gather(
            queryset.filter(**filters).count(),
            queryset.filter(**filters).limit(self.limit).offset(self.offset).order_by(*self.order),
        )
        return PageData(items=items, total=total)

from typing import List

from fastapi import Query


class Paginator:
    """分页器"""

    def __init__(
            self,
            offset: int = Query(0, description="分页参数offset"),
            limit: int = Query(10, description="分页参数limit", ge=0, le=1000)
    ):
        if offset < 0:
            offset = 0
        self.offset = offset
        self.limit = limit

    def get_page_range(self, cur_page, total_page, range_=5):
        offset_ = range_ // 2
        start = cur_page - offset_
        if start <= 0:
            start = 1
        end = start + range_
        if end > total_page:
            end = total_page
        return start, end + 1

    def get_page_data(self, data_list: List, total=None):
        total = total
        next_offset = self.offset + self.limit
        next_offset = next_offset if next_offset < total else total
        has_more = total > next_offset
        cur_page = (self.offset // self.limit) + 1
        total_page = total // self.limit
        if total % self.limit:
            total_page += 1
        page_range = self.get_page_range(cur_page, total_page)
        data = {
            "offset": self.offset,
            "limit": self.limit,
            "data_list": data_list,
            "total": total,
            "has_more": has_more,
            "next_offset": next_offset,
            "cur_page": cur_page,
            "total_page": total_page,
            "page_range": page_range
        }
        return data

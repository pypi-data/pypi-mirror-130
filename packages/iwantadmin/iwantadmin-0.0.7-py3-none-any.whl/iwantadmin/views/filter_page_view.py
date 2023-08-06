from typing import Dict, List

from fastapi import Body, Depends

from iwantadmin.constants.errors import ModelApiError
from iwantadmin.utils.paginator import Paginator
from iwantadmin.views.base import BaseView, ResponseView


class FilterPageModelView(BaseView):
    def __init__(self, manager):
        self.manager = manager
        super().__init__(
            path=".filter.page.get",
            methods=["POST"],
            summary=f"分页条件过滤{self.manager.model_name}"
        )

    @ResponseView()
    async def as_view(
            self,
            filter_params: Dict = Body(..., embed=True),
            orderings: List[str] = Body(None, embed=True),
            paginator: Paginator = Depends()
    ):
        unknow_fields = {param.split('__')[0] for param in filter_params}.difference(
            self.manager.model_cls._meta.fields
        )
        unknow_ordering_fields = {ordering.split("-")[-1] for ordering in orderings}.difference(self.manager.model_cls._meta.fields)
        if unknow_fields or unknow_ordering_fields:
            return ModelApiError.field_not_found.apply(
                model_name=self.manager.model_name,
                unknow_fields=unknow_fields or unknow_ordering_fields
            )
        models = await self.manager.filter_page(filter_params, orderings, paginator.offset, paginator.limit)
        total = None
        if paginator.need_total:
            total = await self.manager.filter_count(filter_params)
        data_list = [model.to_dict() for model in models]
        return paginator.get_page_data(data_list, total)

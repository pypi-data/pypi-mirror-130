from typing import Dict, List

from fastapi import Body

from iwantadmin.constants.errors import ModelApiError
from iwantadmin.views.base import BaseView, ResponseView


class FilterValuesModelView(BaseView):
    def __init__(self, manager):
        self.manager = manager
        super().__init__(
            path=".filter.values.get",
            methods=["POST"],
            summary=f"字段条件过滤{self.manager.model_name}"
        )

    @ResponseView()
    async def as_view(
            self,
            filter_params: Dict = Body(..., embed=True),
            values: List[str] = Body(None, embed=True),
    ):
        unknow_fields = {param.split('__')[0] for param in filter_params}.difference(
            self.manager.model_cls._meta.fields
        )
        unknow_value_fields = set(values).difference(self.manager.model_cls._meta.fields)
        if unknow_fields or unknow_value_fields:
            return ModelApiError.field_not_found.apply(
                model_name=self.manager.model_name,
                unknow_fields=unknow_fields or unknow_value_fields
            )
        total = await self.manager.filter_count(filter_params)
        if total > 1000:
            return ModelApiError.result_set_too_large
        models = await self.manager.filter_values(filter_params, values)
        return {f"{self.manager.model_name}s": models}

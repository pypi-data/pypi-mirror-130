from typing import Dict

from fastapi import Body

from iwantadmin.constants.errors import ModelApiError
from iwantadmin.views.base import BaseView, ResponseView


class FilterModelView(BaseView):
    def __init__(self, manager):
        self.manager = manager
        super().__init__(
            path=".filter.get",
            methods=["POST"],
            summary=f"条件过滤{self.manager.model_name}"
        )

    @ResponseView()
    async def as_view(
            self,
            filter_params: Dict = Body(..., embed=True),
    ):
        unknow_fields = {param.split('__')[0] for param in filter_params}.difference(self.manager.model_cls._meta.fields)
        if unknow_fields:
            return ModelApiError.field_not_found.apply(
                model_name=self.manager.model_name,
                unknow_fields=unknow_fields
            )
        total = await self.manager.filter_count(filter_params)
        if total > 1000:
            return ModelApiError.result_set_too_large
        models = await self.manager.filter(filter_params)
        if not models:
            return ModelApiError.filter_not_found.apply(
                model_name=self.manager.model_name
            )
        return {f"{self.manager.model_name}s": [model.to_dict() for model in models]}

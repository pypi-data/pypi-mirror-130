from typing import Dict

from fastapi import Query, Body

from iwantadmin.constants.errors import ModelApiError
from iwantadmin.views.base import BaseView, ResponseView


class UpdateModelView(BaseView):
    def __init__(self, manager):
        self.manager = manager
        super().__init__(
            path=".edit",
            methods=["POST"],
            summary=f"修改{self.manager.model_name}"
        )

    @ResponseView()
    async def as_view(
            self,
            model_id: int = Query(...),
            info: Dict = Body(..., embed=True)
    ):
        unknow_fields = set(info.keys()).difference(self.manager.model_cls._meta.fields)
        if unknow_fields:
            return ModelApiError.field_not_found.apply(
                model_name=self.manager.model_name,
                unknow_fields=unknow_fields
            )
        flag = await self.manager.update(model_id, info)
        if not flag:
            return ModelApiError.update_fail.apply(
                model_id=model_id,
                model_name=self.manager.model_name
            )
        return dict(success=flag)

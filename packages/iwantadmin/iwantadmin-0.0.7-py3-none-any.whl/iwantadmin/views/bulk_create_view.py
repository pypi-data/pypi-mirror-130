from typing import Dict, List

from fastapi import Body

from iwantadmin.constants.errors import ModelApiError
from iwantadmin.views.base import BaseView, ResponseView


class BulkCreateModelView(BaseView):
    def __init__(self, manager):
        self.manager = manager
        super().__init__(
            path=".batch.add",
            methods=["POST"],
            summary=f"批量创建{self.manager.model_name}"
        )

    @ResponseView()
    async def as_view(
            self,
            infos: List[Dict] = Body(..., embed=True)
    ):
        for info in infos:
            unknow_fields = set(info.keys()).difference(self.manager.model_cls._meta.fields)
            if unknow_fields:
                return ModelApiError.field_not_found.apply(
                    model_name=self.manager.model_name,
                    unknow_fields=unknow_fields
                )
        success = await self.manager.bulk_create(infos)
        if not success:
            return ModelApiError.bulk_create_fail.apply(
                model_name=self.manager.model_name
            )
        return dict(success=success)

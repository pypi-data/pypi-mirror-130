from fastapi import Query

from iwantadmin.constants.errors import ModelApiError
from iwantadmin.views.base import BaseView, ResponseView


class GetModelView(BaseView):
    def __init__(self, manager):
        self.manager = manager
        super().__init__(
            path=".get",
            methods=["GET"],
            summary=f"查询单个{self.manager.model_name}"
        )

    @ResponseView()
    async def as_view(
            self,
            model_id: int = Query(...)
    ):
        model = await self.manager.get(model_id)
        if not model:
            return ModelApiError.get_not_found.apply(model_id=model_id, model_name=self.manager.model_name)
        return {self.manager.model_name: model.to_dict()}

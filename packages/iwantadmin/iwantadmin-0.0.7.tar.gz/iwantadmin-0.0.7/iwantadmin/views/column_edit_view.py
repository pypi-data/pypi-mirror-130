from fastapi.params import Path
from starlette.requests import Request

from iwantadmin.views.base import BaseView
from iwantadmin.views.tables_view import tables, templates


class ColumnEditView(BaseView):
    def __init__(self):
        super().__init__(
            path="/{model_name}/{model_id}/edit",
            methods=["POST"],
            summary=f"行数据编辑",
            name="column_edit"
        )

    async def as_view(
        self,
        request: Request,
        model_name: str = Path(""),
        model_id: int = Path("id")
    ):
        data = await request.form()
        data = dict(**data)
        if "id" in data.keys():
            del data["id"]
        model = tables.get(model_name)
        if not model:
            return "MODEL NOT FOUND"
        obj = await model.admin_manager.get(model_id)
        if not obj:
            return templates.TemplateResponse("404.html", dict(request=request))
        if await model.admin_manager.update(model_id, data):
            for k, v in data.items():
                setattr(obj, k, v)
        return templates.TemplateResponse(
            "column_detail.html",
            dict(
                view=self,
                request=request,
                tables=tables.keys(),
                model_name=model_name,
                obj=obj
            )
        )

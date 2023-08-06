from fastapi.params import Path
from starlette.requests import Request

from iwantadmin.views.base import BaseView
from iwantadmin.views.tables_view import tables, templates


class ColumnAddView(BaseView):
    def __init__(self):
        super().__init__(
            path="/{model_name}/add",
            methods=["GET", "POST"],
            summary=f"行数据编辑",
            name="column_add"
        )

    async def as_view(
        self,
        request: Request,
        model_name: str = Path("")
    ):
        data = await request.form()
        data = dict(**data)
        if "id" in data.keys():
            del data["id"]
        model = tables.get(model_name)
        if not model:
            return "MODEL NOT FOUND"
        if data:
            obj = await model.admin_manager.create(data)
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
        else:
            obj = model()
            return templates.TemplateResponse(
                "column_add.html",
                dict(
                    view=self,
                    request=request,
                    tables=tables.keys(),
                    model_name=model_name,
                    obj=obj
                )
            )

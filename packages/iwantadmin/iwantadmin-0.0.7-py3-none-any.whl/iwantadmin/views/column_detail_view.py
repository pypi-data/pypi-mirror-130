from fastapi.params import Path
from starlette.requests import Request

from iwantadmin.views.base import BaseView
from iwantadmin.views.tables_view import tables, templates


class ColumnDetailView(BaseView):
    def __init__(self):
        super().__init__(
            path="/{model_name}/{model_id}/info",
            methods=["GET"],
            summary=f"行数据详情页",
            name="column_detail"
        )

    async def as_view(
        self,
        request: Request,
        model_name: str = Path(""),
        model_id: int = Path("id")
    ):
        model = tables.get(model_name)
        if not model:
            return "MODEL NOT FOUND"
        obj = await model.admin_manager.get(model_id)
        if not obj:
            return templates.TemplateResponse("404.html", dict(request=request))
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

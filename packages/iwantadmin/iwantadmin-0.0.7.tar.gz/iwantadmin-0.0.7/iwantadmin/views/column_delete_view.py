from fastapi.params import Path
from starlette.requests import Request
from starlette.responses import RedirectResponse

from iwantadmin.views.base import BaseView
from iwantadmin.views.tables_view import tables, templates


class ColumnDeleteView(BaseView):
    def __init__(self):
        super().__init__(
            path="/{model_name}/{model_id}/delete",
            methods=["GET"],
            summary=f"行数据删除",
            name="column_delete"
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
        await obj.delete()
        return RedirectResponse(f"{request.app.state.admin_prefix}?model_name={model_name}")

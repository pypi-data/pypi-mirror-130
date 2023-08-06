from fastapi.params import Depends, Query
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from iwantadmin.constants.const import CUR_DIR
from iwantadmin.utils.paginator import Paginator
from iwantadmin.views.base import BaseView

templates = Jinja2Templates(directory=f"{CUR_DIR}/templates")
tables = dict()


class GetTablesView(BaseView):
    def __init__(self):
        super().__init__(
            path="/",
            methods=["GET"],
            summary=f"首页",
            name="admin_index"
        )

    async def as_view(
        self,
        request: Request,
        model_name: str = Query(""),
        ordering: str = Query("id"),
        paginator: Paginator = Depends()
    ):
        if not model_name and tables:
            model_name = list(tables.keys())[0]
        model = tables.get(model_name)
        if not model:
            return "MODEL NOT FOUND"
        objects = await model.admin_manager.filter_page(
            dict(), [ordering], offset=paginator.offset, limit=paginator.limit
        )
        total = await model.admin_manager.filter_count(dict())
        page_data = paginator.get_page_data(objects, total)
        return templates.TemplateResponse(
            "index.html",
            dict(
                view=self,
                request=request,
                tables=tables.keys(),
                model_name=model_name,
                objects=objects,
                **page_data
            )
        )

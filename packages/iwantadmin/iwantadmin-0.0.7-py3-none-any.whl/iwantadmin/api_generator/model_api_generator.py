import inspect

from fastapi import APIRouter
from tortoise.models import Model
from iwantadmin.managers.base import BaseManager

from iwantadmin.views.base import BaseView


class ModelApiGenerator(object):

    def __init__(self, model: Model):
        self.manager: BaseManager = model.admin_manager

    def bind_entry(self, manager_api_entry):
        """
        初始化manager对应的router
        """
        router = APIRouter()
        for api_view in self.manager.exposed_apis():
            if inspect.isclass(api_view) and issubclass(api_view, BaseView):
                api_view(self.manager).bind_router(router)

        _prefix = f"/{self.manager.model_name}"
        _tag = f"{self.manager.model_name} manager api"
        manager_api_entry.include_router(
            router,
            prefix=_prefix,
            tags=[_tag]
        )

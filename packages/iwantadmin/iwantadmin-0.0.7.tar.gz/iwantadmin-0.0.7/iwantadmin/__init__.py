__version_info__ = (0, 0, 1)
__version__ = '{0}.{1}.{2}'.format(*__version_info__)

import logging

from fastapi import FastAPI, APIRouter
from tortoise.models import Model

from iwantadmin.api_generator.model_api_generator import ModelApiGenerator
from iwantadmin.managers.base import BaseManager
from iwantadmin.utils.patch import install_patch
from iwantadmin.views.tables_view import tables, GetTablesView
from iwantadmin.views.column_add_view import ColumnAddView
from iwantadmin.views.column_detail_view import ColumnDetailView
from iwantadmin.views.column_edit_view import ColumnEditView
from iwantadmin.views.column_delete_view import ColumnDeleteView

logger = logging.getLogger(__name__)
admin_router = APIRouter()
install_patch()


def init(app: FastAPI, prefix=""):
    GetTablesView().bind_router(admin_router)
    ColumnDetailView().bind_router(admin_router)
    ColumnEditView().bind_router(admin_router)
    ColumnDeleteView().bind_router(admin_router)
    ColumnAddView().bind_router(admin_router)
    prefix = f"{prefix}/admin"
    app.include_router(admin_router, prefix=prefix)
    app.state.admin_prefix = prefix


def admin(model: Model):
    model.admin_manager = BaseManager(model_cls=model)
    tables[model.admin_manager.model_name] = model
    manager_apis = ModelApiGenerator(model)
    manager_apis.bind_entry(admin_router)
    return model


# if __name__ == '__main__':
#     import django

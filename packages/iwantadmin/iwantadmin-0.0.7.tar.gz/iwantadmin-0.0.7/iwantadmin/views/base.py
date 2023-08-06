import abc
import functools
import logging
import time

from typing import Dict
from fastapi.routing import APIRoute

from iwantadmin.constants.errors import ErrorNode

logger = logging.getLogger(__name__)


class ResponseView(object):

    def __call__(self, func):
        @functools.wraps(func)
        async def decorated(view, *args, **kwargs):
            self.view = view
            result = await func(view, *args, **kwargs)
            if isinstance(result, ErrorNode):
                return self.fail(result)
            return self.success(result)
        return decorated

    def success(self, data):
        return self.response(data)

    def fail(self, error_node):
        return self.response(**error_node.to_dict())

    def response(self, data: Dict = None, code="0000", message="SUCCESS"):
        if data is None:
            data = dict()
        if not isinstance(data, dict):
            logger.exception(f"{self.view.__class__.__name__} 返回值类型异常")
            data = {
                "temp_data": data
            }
        cur_ts = int(time.time())  # 服务器时间
        return dict(
            cur_ts=cur_ts,
            code=code,
            message=message,
            data=data
        )


class BaseView(metaclass=abc.ABCMeta):
    def __init__(
            self,
            path,
            response_model=None,
            dependencies=None,
            summary=None,
            methods=None,
            deprecated=False,
            **kwargs
    ):
        self.path = path
        self.end_point = self.as_view
        self.response_model = response_model
        self.dependencies = dependencies
        self.summary = summary
        self.methods = methods or ["GET"]
        self.deprecated = deprecated
        self.kwargs = kwargs

    def bind_router(self, router):
        route = APIRoute(
            path=self.path,
            endpoint=self.as_view,
            response_model=self.response_model,
            dependencies=self.dependencies,
            summary=self.summary,
            methods=self.methods,
            deprecated=self.deprecated,
            **self.kwargs
        )
        router.routes.append(route)

    @abc.abstractmethod
    async def as_view(
            self,
            *args,
            **kwargs
    ):
        ...

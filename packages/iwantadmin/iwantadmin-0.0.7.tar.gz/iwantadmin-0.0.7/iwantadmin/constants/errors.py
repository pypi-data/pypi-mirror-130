import copy


class ErrorNode:
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def unpack(self):
        return self.code, self.message

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message
        }

    def apply(self, *args, **kwargs):
        _node = copy.deepcopy(self)
        _node.message = _node.message.format(*args, **kwargs)
        return _node

    def to_exception(self):
        return Exception(self.code, self.message)


class Error:
    success = ErrorNode("0000", "success")
    timeout_error = ErrorNode("9999", "timeout")
    code_not_found = ErrorNode("ffff", "code not found")
    request_error = ErrorNode("FFFF", "request error")



class ModelApiError(Error):
    create_fail = ErrorNode("10000", "{model_name}创建失败")
    bulk_create_fail = ErrorNode("10001", "{model_name}批量创建失败")
    get_not_found = ErrorNode("10002", "{model_name}[{model_id}]不存在")
    filter_not_found = ErrorNode("10003", "没有符合条件的{model_name}")
    update_fail = ErrorNode("10004", "{model_name}[{model_id}]更新失败，目标不存在或内容无变化")
    field_not_found = ErrorNode("10005", "{model_name}中没有{unknow_fields}字段")
    result_set_too_large = ErrorNode("10006", "结果集过大，请使用分页查询")

from tortoise.models import Model


def fields_dict(model: Model):
    fields = model._meta.fields
    dic = {
        field: getattr(model, field)
        for field in fields
        if hasattr(model, field)
    }
    return dic

def to_dict(model: Model, *args, **kwargs):
    """model对外返回"""
    return model.fields_dict()


def install_patch():
    Model.fields_dict = fields_dict
    Model.to_dict = to_dict

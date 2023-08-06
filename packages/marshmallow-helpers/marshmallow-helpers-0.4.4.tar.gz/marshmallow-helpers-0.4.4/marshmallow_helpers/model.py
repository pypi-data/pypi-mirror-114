from collections import OrderedDict

import attr
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declared_attr

from .marsh_schema import attr_with_schema


def model_with_schema(maybe_cls=None, **kwargs):
    """Make the sqlalchemy class an attr.s
    Also, updates annotations for `declared_attr`s
    """
    def decorator(cls):
        these = OrderedDict()
        these_with_defaults = {}
        if not hasattr(cls, "__annotations__"):
            cls.__annotations__ = {}
        for name, column in inspect(cls).columns.items():
            if column.nullable:
                these_with_defaults[name] = attr.ib(default=None)
            else:
                these[name] = attr.ib()
            if name in cls.__annotations__:
                continue

            try:
                tp = column.type.python_type
            except NotImplementedError:
                pass
            else:
                cls.__annotations__[name] = tp
                continue

            for base in cls.__bases__:
                if name not in base.__dict__:
                    continue
                if not isinstance(base.__dict__[name], declared_attr):
                    continue
                cls.__annotations__[name] = base.__dict__[
                    name].fget.__annotations__['return']

        these.update(these_with_defaults)

        return attr_with_schema(
            **{"register_as_scheme": True, "strict": True, **kwargs})(
                attr.s(cls, these=these, init=False))

    if maybe_cls is None:
        return decorator
    else:
        return decorator(maybe_cls)

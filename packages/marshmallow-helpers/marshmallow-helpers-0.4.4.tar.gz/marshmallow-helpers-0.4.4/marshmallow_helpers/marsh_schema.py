import attr
from copy import copy
from functools import wraps

from .marshmallow_annotations.ext.attrs import AttrsSchema


def attr_with_schema(**kwargs):
    def decorator(cls):
        bases = []
        if hasattr(cls, 'Schema'):
            bases.append(cls.Schema)
        bases.append(AttrsSchema)

        schema_meta = getattr(cls, 'SchemaMeta', object)
        fields = attr.fields(cls)

        class Schema(*bases):
            class Meta(schema_meta):
                locals().update(kwargs)
                target = cls

        for field in fields:
            if field.default == attr.NOTHING:
                Schema._declared_fields[field.name].required = True

        cls.schema = Schema
        Schema.__name__ = cls.__name__ + "Schema"

        def attr_iter(self):
            return iter(self.__dict__.items())

        cls.__iter__ = attr_iter
        return cls
    return decorator


def derive(from_,
           *,
           exclude=None,
           derive_schema=True,
           derive_schema_meta=True):
    if exclude is None:
        exclude = []
    exclude = set(exclude)

    def decorator(cls):
        @wraps(cls, updated=[])
        class Wrapped(cls):
            locals().update({attr.name: attr.default
                             for attr in from_.__attrs_attrs__
                             if attr.name not in exclude})
        Wrapped.__annotations__ = copy(getattr(cls, '__annotations__', {}))
        for k in Wrapped.__annotations__.keys():
            if hasattr(cls, k):
                setattr(Wrapped, k, getattr(cls, k))
        if derive_schema and hasattr(from_, 'Schema'):
            if hasattr(cls, 'Schema'):
                class Schema(cls.Schema, from_.Schema):
                    pass
            else:
                Schema = from_.Schema
            Wrapped.Schema = Schema

        if derive_schema_meta and hasattr(from_, 'SchemaMeta'):
            if hasattr(cls, 'SchemaMeta'):
                class SchemaMeta(cls.SchemaMeta, from_.SchemaMeta):
                    pass
            else:
                SchemaMeta = from_.SchemaMeta
            Wrapped.SchemaMeta = SchemaMeta

        Wrapped.__annotations__.update({attr.name: attr.type
                                        for attr in from_.__attrs_attrs__
                                        if attr.name not in exclude})
        return Wrapped
    return decorator

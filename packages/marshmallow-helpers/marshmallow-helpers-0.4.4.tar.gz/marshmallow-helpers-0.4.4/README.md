This library helps to create marshmallow schemas easier.


## Run flask locally

```
export FLASK_APP=demo_app.flask_app
flask run
```

## Testing

Run the following:
```
python -m pytest tests
```

## Usage

### Enums

Derive from RegisteredEnum class to have serializable enum. Set `__load_by_value__` and `__dump_by_value__` to correspondingly load and dump enumerations by their keys or values. Set `__by_value__` for both of them. Default values are `True`.

```
Class Letter(RegisteredEnum):
    __load_by_value__ = False

    a = 'First letter'
    b = 'Second letter'
    ...
```

If request and response schemas have Enum in their fields, you can request a letter and see the value of it, e.g. requesting `a` you will get `First letter`.

Register EnumField to api with
```
api.register_field(EnumField, 'string', None)
```

### Add schema on attrs

Decorate your class with `@attr_with_schema` to add a schema on `@attr.s` class. It will be stored on `class.schema`.

```
@attr_with_schema(register_as_scheme=True, strict=True)
@attr.s(auto_attribs=True)
class Attributes:
    integer: int
    string: str
    obj: dict
```

#### Adding validators on the schema

```
@attr_with_schema(register_as_scheme=True, strict=True)
@attr.s(auto_attribs=True)
class Attributes:
    nonnegative_integer: int
    string: str
    obj: dict

    class Schema:
        @ma.validates_schema
        def validate_nonnegative_integer(self, data, **kwargs):
            if data["nonnegative_integer"] < 0:
                raise ma.ValidationError(
                    "nonnegative_integer should be non-negative")
```

#### Adding meta information on the schema

```
@attr_with_schema(register_as_scheme=True, strict=True)
@attr.s(auto_attribs=True)
class Attributes:
    nonnegative_integer: int
    string: str
    obj: dict

    class SchemaMeta:
        class Fields:
            obj = {"allow_none": True}
```

### Derive

To derive from an `attrs` class use `derive` decorator. Here is an example:
```
@attr_with_schema(register_as_scheme=True, strict=True)
@attr.s(auto_attribs=True)
class Base:
    obj: dict
    integer: int = 0
    prime: bool = False

    class SchemaMeta:
        class Fields:
            obj = {"allow_none": True}
            integer = {"allow_none": True,
                       "validate": ma.validate.Range(min=0, max=100)}

    class Schema:
        @ma.validates_schema
        def prime_integer(self, data, **kwargs):
            if data["prime"] and not self.is_prime(data['integer']):
                raise ma.ValidationError("integer was supposed to be prime")

        @staticmethod
        def is_prime(num):
            for i in range(2, num - 1):
                if num % i == 0:
                    return False
            return True


@attr_with_schema(register_as_scheme=True, strict=True)
@attr.s(auto_attribs=True)
@derive(Base, exclude={"obj"})
class Derived:
    string: str
```

Note, that `@derive` should be called first. `derive` get an additional `exclude` argument, which excludes already existing attributes from base class(it doesn't exclude from current class).
The `Derived` class above is equivalent to the following:
```
@attr_with_schema(register_as_scheme=True, strict=True)
@attr.s(auto_attribs=True)
class Derived:
    string: str
    integer: int = 0
    prime: bool = False

    class SchemaMeta:
        class Fields:
            obj = {"allow_none": True}
            integer = {"allow_none": True,
                       "validate": ma.validate.Range(min=0, max=100)}

    class Schema:
        @ma.validates_schema
        def prime_integer(self, data, **kwargs):
            if data["prime"] and not self.is_prime(data['integer']):
                raise ma.ValidationError("integer was supposed to be prime")

        @staticmethod
        def is_prime(num):
            for i in range(2, num - 1):
                if num % i == 0:
                    return False
            return True
```

WARNING: derive also derives schemas and validations. The @validate_schema might use `obj` in the validation. In that case pass `derive_schema=False` or `derive_schema_meta=False` to `derive` decorator to not derive corresponding schemas.

### Sqlalchemy models
To add a marshmallow schema to sqlalchemy model use `model_with_schema` decorator:

```
@model_with_schema
class Table(db.Model):
    __tablename__ = 'table'
    column = Column(String, primary_key=True)
    letter = Column(Letter)
    dictionary = Column(JSON)
    array: List[str] = Column(JSON)
```

The created marshmallow schema is stored on `Table.schema`. Here, `array` will be loaded as `list` and `dictionary` will be loaded as `dict`.

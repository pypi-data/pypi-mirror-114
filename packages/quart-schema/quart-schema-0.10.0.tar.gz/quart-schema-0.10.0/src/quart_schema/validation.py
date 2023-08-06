from __future__ import annotations

from dataclasses import asdict, is_dataclass
from enum import auto, Enum
from functools import wraps
from typing import Any, Callable, cast, Optional, Union

from pydantic import BaseModel, ValidationError
from pydantic.dataclasses import dataclass as pydantic_dataclass, is_builtin_dataclass
from pydantic.schema import model_schema
from quart import current_app, request, ResponseReturnValue as QuartResponseReturnValue
from werkzeug.datastructures import Headers
from werkzeug.exceptions import BadRequest

from .typing import PydanticModel, ResponseReturnValue

QUART_SCHEMA_REQUEST_ATTRIBUTE = "_quart_schema_request_schema"
QUART_SCHEMA_RESPONSE_ATTRIBUTE = "_quart_schema_response_schemas"
QUART_SCHEMA_QUERYSTRING_ATTRIBUTE = "_quart_schema_querystring_schema"


class SchemaInvalidError(Exception):
    pass


class ResponseSchemaValidationError(Exception):
    def __init__(self, validation_error: Optional[ValidationError] = None) -> None:
        self.validation_error = validation_error


class RequestSchemaValidationError(BadRequest):
    def __init__(self, validation_error: Union[TypeError, ValidationError]) -> None:
        super().__init__()
        self.validation_error = validation_error


class DataSource(Enum):
    FORM = auto()
    JSON = auto()


def validate_querystring(model_class: PydanticModel) -> Callable:
    """Validate the querystring arguments.

    This ensures that the query string arguments can be converted to
    the *model_class*. If they cannot a `RequestSchemaValidationError`
    is raised which by default results in a 400 response.

    Arguments:
        model_class: The model to use, either a dataclass, pydantic
            dataclass or a class that inherits from pydantic's
            BaseModel. All the fields must be optional.
    """
    if is_builtin_dataclass(model_class):
        model_class = pydantic_dataclass(model_class)

    schema = model_schema(model_class)

    if len(schema.get("required", [])) != 0:
        raise SchemaInvalidError("Fields must be optional")

    def decorator(func: Callable) -> Callable:
        setattr(func, QUART_SCHEMA_QUERYSTRING_ATTRIBUTE, model_class)

        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                model = model_class(**request.args)
            except (TypeError, ValidationError) as error:
                raise RequestSchemaValidationError(error)
            else:
                return await current_app.ensure_async(func)(*args, query_args=model, **kwargs)

        return wrapper

    return decorator


def validate_request(
    model_class: PydanticModel,
    *,
    source: DataSource = DataSource.JSON,
) -> Callable:
    """Validate the request data.

    This ensures that the request body is JSON and that the body can
    be converted to the *model_class*. If they cannot a
    `RequestSchemaValidationError` is raised which by default results
    in a 400 response.

    Arguments:
        model_class: The model to use, either a dataclass, pydantic
            dataclass or a class that inherits from pydantic's
            BaseModel. All the fields must be optional.
        source: The source of the data to validate (json or form
            encoded).
    """
    if is_builtin_dataclass(model_class):
        model_class = pydantic_dataclass(model_class)

    schema = model_schema(model_class)
    if source == DataSource.FORM and any(
        schema["properties"][field]["type"] == "object" for field in schema["properties"]
    ):
        raise SchemaInvalidError("Form must not have nested objects")

    def decorator(func: Callable) -> Callable:
        setattr(func, QUART_SCHEMA_REQUEST_ATTRIBUTE, (model_class, source))

        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            if source == DataSource.JSON:
                data = await request.get_json()
            else:
                data = await request.form

            try:
                model = model_class(**data)
            except (TypeError, ValidationError) as error:
                raise RequestSchemaValidationError(error)
            else:
                return await current_app.ensure_async(func)(*args, data=model, **kwargs)

        return wrapper

    return decorator


def validate_response(model_class: PydanticModel, status_code: int = 200) -> Callable:
    """Validate the response data.

    This ensures that the response is a either dictionary that the
    body can be converted to the *model_class* or an instance of the
    *model_class*. If this is not possible a
    `ResponseSchemaValidationError` is raised which by default results
    in a 500 response. The returned value is then a dictionary which
    Quart encodes as JSON.

    Arguments:
        model_class: The model to use, either a dataclass, pydantic
            dataclass or a class that inherits from pydantic's
            BaseModel. All the fields must be optional.
        status_code: The status code this validation applies
            to. Defaults to 200.
    """
    if is_builtin_dataclass(model_class):
        model_class = pydantic_dataclass(model_class)

    def decorator(
        func: Callable[..., ResponseReturnValue]
    ) -> Callable[..., QuartResponseReturnValue]:
        schemas = getattr(func, QUART_SCHEMA_RESPONSE_ATTRIBUTE, {})
        schemas[status_code] = model_class
        setattr(func, QUART_SCHEMA_RESPONSE_ATTRIBUTE, schemas)

        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = await current_app.ensure_async(func)(*args, **kwargs)

            status_or_headers = None
            headers = None
            if isinstance(result, tuple):
                value, status_or_headers, headers = result + (None,) * (3 - len(result))
            else:
                value = result

            status = 200
            if status_or_headers is not None and not isinstance(
                status_or_headers, (Headers, dict, list)
            ):
                status = int(status_or_headers)

            if status == status_code:
                if isinstance(value, dict):
                    try:
                        model_value = model_class(**value)
                    except ValidationError as error:
                        raise ResponseSchemaValidationError(error)
                elif type(value) == model_class:
                    model_value = value
                elif is_builtin_dataclass(value):
                    model_value = model_class(**asdict(value))
                else:
                    raise ResponseSchemaValidationError()
                if is_dataclass(model_value):
                    return asdict(model_value), status_or_headers, headers
                else:
                    model_value = cast(BaseModel, model_value)
                    return model_value.dict(), status_or_headers, headers
            else:
                return result

        return wrapper

    return decorator

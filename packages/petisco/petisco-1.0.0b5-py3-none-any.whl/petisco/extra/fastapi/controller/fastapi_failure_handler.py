from typing import Dict

from fastapi import HTTPException
from meiga import Result

from petisco.base.domain.errors.domain_error import DomainError
from petisco.base.application.controller.http_error import (
    DEFAULT_HTTP_ERROR_DETAIL,
    HttpError,
)


def fastapi_failure_handler(result: Result, error_map: Dict[type, HttpError]):
    domain_error = result.value
    error_type = type(domain_error)
    http_error = error_map.get(error_type, HttpError())

    detail = "Unknown Error"
    if isinstance(domain_error, DomainError):
        detail = (
            http_error.detail
            if http_error.detail != DEFAULT_HTTP_ERROR_DETAIL
            else domain_error.detail()
        )
    raise HTTPException(status_code=http_error.status_code, detail=detail)

from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.application.exceptions import(
    BusinessRuleError,
    ConflictError,
    ResourceNotFoundError,
    AccessDeniedError,
)



async def resourse_not_found_handler(
    request: Request,
    exc: ResourceNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )

async def access_denied_handler(
    request: Request,
    exc: AccessDeniedError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": str(exc)},
    )

async def conflict_handler(
    request: Request,
    exc: ConflictError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )

async def business_rule_handler(
    request: Request,
    exc: BusinessRuleError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )
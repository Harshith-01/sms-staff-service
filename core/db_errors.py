import re
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


def _clean(text: str | None) -> str:
    if not text:
        return ""
    return " ".join(str(text).split())


def _field_from_detail(detail: str | None) -> str | None:
    if not detail:
        return None
    match = re.search(r"\(([^)]+)\)=", detail)
    if not match:
        return None
    return match.group(1)


def db_integrity_http_exception(
    exc: IntegrityError,
    fallback_status: int = 409,
    fallback_detail: str = "Database constraint violation",
) -> HTTPException:
    orig = getattr(exc, "orig", None)
    diag = getattr(orig, "diag", None)

    pgcode = getattr(orig, "pgcode", None)
    detail = _clean(getattr(diag, "message_detail", None)) or _clean(str(orig))
    column_name = getattr(diag, "column_name", None)
    constraint_name = getattr(diag, "constraint_name", None)

    field = column_name or _field_from_detail(detail)

    if pgcode == "23502":
        msg = f"Field '{field}' cannot be null" if field else "A required field cannot be null"
        if detail:
            msg = f"{msg}. {detail}"
        return HTTPException(status_code=400, detail=msg)

    if pgcode == "23505":
        msg = "Duplicate value violates a unique constraint"
        if constraint_name:
            msg = f"{msg}: {constraint_name}"
        if detail:
            msg = f"{msg}. {detail}"
        return HTTPException(status_code=409, detail=msg)

    if pgcode == "23503":
        msg = "Related record not found or still referenced (foreign key violation)"
        if constraint_name:
            msg = f"{msg}: {constraint_name}"
        if detail:
            msg = f"{msg}. {detail}"
        return HTTPException(status_code=409, detail=msg)

    if pgcode == "23514":
        msg = "Input violates a database check constraint"
        if constraint_name:
            msg = f"{msg}: {constraint_name}"
        if detail:
            msg = f"{msg}. {detail}"
        return HTTPException(status_code=400, detail=msg)

    if pgcode == "22001":
        msg = f"Field '{field}' exceeds allowed length" if field else "Input exceeds allowed length"
        if detail:
            msg = f"{msg}. {detail}"
        return HTTPException(status_code=400, detail=msg)

    if detail:
        return HTTPException(status_code=fallback_status, detail=f"{fallback_detail}. {detail}")

    return HTTPException(status_code=fallback_status, detail=fallback_detail)

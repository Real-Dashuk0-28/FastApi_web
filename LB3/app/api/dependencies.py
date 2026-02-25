from fastapi import Request, HTTPException, Query, Header
from LB3.app.core.config import TOKENS


UNSAFE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})


def verify_token(
    request: Request,
    api_token: str = Header(None, alias="x-auth-token")):
    if request.method in UNSAFE_METHODS:
        if not api_token or api_token not in TOKENS:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized"
            )
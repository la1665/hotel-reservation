from fastapi import HTTPException
from typing import Dict


class BadRequestExceptions(HTTPException):
    def __init__(self, detail: str) -> None:
        self.detail = detail


class NotAllowedException(HTTPException):
    def __init__(self, name: str, detail: str) -> None:
        self.name = name
        self.detail = detail


class NotFoundException(HTTPException):
    def __init__(self, resource: str) -> None:
        self.resource = resource


class UnauthorizedException(HTTPException):
    def __init__(self, name, detail, headers: Dict[str, str]):
        self.name = name
        self.detail = detail
        self.headers = headers

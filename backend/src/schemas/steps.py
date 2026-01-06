from pydantic import BaseModel


class Steps(BaseModel):
    data: list[str]

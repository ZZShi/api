from pydantic import BaseModel


class CreateEvent(BaseModel):
    name: str
    age: int

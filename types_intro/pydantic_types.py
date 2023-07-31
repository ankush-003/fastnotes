from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    id: int
    name: str
    age: int
    birthdate: date | None = None
    created_at: str = date.today().strftime("%Y-%m-%d")

external_data = {
    "id": "123",
    "name": "John Doe",
    "age": "32",
    "birthdate": "1988-01-01",
}

user = User(**external_data)
print(user)
print(user.birthdate)
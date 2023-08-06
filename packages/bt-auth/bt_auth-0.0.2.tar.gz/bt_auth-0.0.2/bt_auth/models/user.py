from typing import Optional, List

from pydantic import BaseModel

from bt_auth.resources.enums import UserStatus


class User(BaseModel):
    id: int
    email: str
    firstname: str
    lastname: str
    image: Optional[str]
    default_competition: Optional[int]
    default_area: Optional[int]
    phone_number: Optional[str]
    organization: Optional[str]
    status: UserStatus
    areas: List[int]
    competitions: List[int]
    pass

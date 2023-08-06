from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
	username: str
	given_name: Optional[str]
	family_name: Optional[str]
	email: Optional[str]
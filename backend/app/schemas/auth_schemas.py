from pydantic import BaseModel, ConfigDict

class Token(BaseModel):
    access_token: str
    token_type: str



class TokenData(BaseModel):
    username: str | None = None


class UserAccount(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    


class AuthResponse(BaseModel):
    user: UserAccount
    token: Token


class UserInDB(UserAccount):
    hashed_password: str
from typing import Annotated
from pydantic import BaseModel
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username:str
    email:str
    full_name:str

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user

@app.get("/item")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

if __name__== "__main__":
    import uvicorn
    uvicorn.run(app,host="localhost",port=8001)
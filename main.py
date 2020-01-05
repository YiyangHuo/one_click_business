from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.requests import Request

from auth import *
from data_schema import *
import databaseapi as db
from exceptions import make_401_exception
from middleware import log_action

app = FastAPI()


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password, form_data.scopes)
    if not user:
        raise make_401_exception("Incorrect username or password or requesting invalid permission", "Bearer")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Security(get_current_user, scopes=["me"])):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: User = Security(get_current_user, scopes=["items"])
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.get("/status/")
async def read_system_status(user: User = Depends(get_current_user)):
    return {"status": "ok"}

@app.post("/api/signup")
async def user_signup(user: UserFull, request: Request):
    log_action(request.client.host, user.username, "Sign Up", None)

    user.hashed_password = get_password_hash(user.hashed_password)
    db.PutUser(vars(user))
    return 200

@app.get('/admin/log')
async def get_log():
    r = db.GetLog()
    print(r[0])
    return {'data': r}
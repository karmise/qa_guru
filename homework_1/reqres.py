import json
from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from homework_1.models.AppStatus import AppStatus
from homework_1.models.user import User
from fastapi_pagination import Page, add_pagination, paginate


app = FastAPI()
add_pagination(app)
users: list[User] = []


@app.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(users=bool(users))


@app.get("/api/users/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    if user_id > len(users):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return users[user_id - 1]


@app.get("/api/users", response_model=Page[User], status_code=HTTPStatus.OK)
def get_users():
    return paginate(users)


if __name__ == "__main__":
    with open("users.json") as f:
        users = json.load(f)

    for user in users:
        User.model_validate(user)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
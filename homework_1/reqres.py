import json
from http import HTTPStatus

from fastapi import FastAPI, Query, HTTPException
from datetime import datetime, timezone

from homework_1.models.user import User

app = FastAPI()

users: list[User]


@app.get("/api/users/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    if user_id > len(users):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return users[user_id - 1]


@app.get("/api/users", status_code=HTTPStatus.OK)
def get_users() -> list[User]:
    return users


@app.post("/api/users")
def create_user(user: dict):
    return {
        "name": user.get("name"),
        "job": user.get("job"),
        "id": 811,
        "createdAt": datetime.now(timezone.utc).isoformat()
    }


if __name__ == "__main__":
    with open("users.json") as f:
        users = json.load(f)

    for user in users:
        User.model_validate(user)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
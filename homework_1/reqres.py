from fastapi import FastAPI, Query
from datetime import datetime, timezone

app = FastAPI()


@app.get("/api/users")
def get_users(page: int = Query(1)):
    if page == 2:
        return {
            "page": 2,
            "per_page": 6,
            "total": 12,
            "total_pages": 2,
            "data": [
                {
                    "id": 7,
                    "email": "michael.lawson@reqres.in",
                    "first_name": "Michael",
                    "last_name": "Lawson",
                    "avatar": "https://reqres.in/img/faces/7-image.jpg"
                },
                {
                    "id": 8,
                    "email": "lindsay.ferguson@reqres.in",
                    "first_name": "Lindsay",
                    "last_name": "Ferguson",
                    "avatar": "https://reqres.in/img/faces/8-image.jpg"
                },
                {
                    "id": 9,
                    "email": "tobias.funke@reqres.in",
                    "first_name": "Tobias",
                    "last_name": "Funke",
                    "avatar": "https://reqres.in/img/faces/9-image.jpg"
                },
                {
                    "id": 10,
                    "email": "byron.fields@reqres.in",
                    "first_name": "Byron",
                    "last_name": "Fields",
                    "avatar": "https://reqres.in/img/faces/10-image.jpg"
                },
                {
                    "id": 11,
                    "email": "george.edwards@reqres.in",
                    "first_name": "George",
                    "last_name": "Edwards",
                    "avatar": "https://reqres.in/img/faces/11-image.jpg"
                },
                {
                    "id": 12,
                    "email": "rachel.howell@reqres.in",
                    "first_name": "Rachel",
                    "last_name": "Howell",
                    "avatar": "https://reqres.in/img/faces/12-image.jpg"
                }
            ],
            "support": {
                "url": "https://contentcaddy.io?utm_source=reqres&utm_medium=json&utm_campaign=referral",
                "text": "Tired of writing endless social media content? Let Content Caddy generate it for you."
            }
        }
    return {"page": page, "data": []}


@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    if user_id == 2:
        return {
            "data": {
                "id": 2,
                "email": "janet.weaver@reqres.in",
                "first_name": "Janet",
                "last_name": "Weaver",
                "avatar": "https://reqres.in/img/faces/2-image.jpg"
            },
            "support": {
                "url": "https://contentcaddy.io?utm_source=reqres&utm_medium=json&utm_campaign=referral",
                "text": "Tired of writing endless social media content? Let Content Caddy generate it for you."
            }
        }
    return {"error": "User not found"}


@app.post("/api/users")
def create_user(user: dict):
    return {
        "name": user.get("name"),
        "job": user.get("job"),
        "id": 811,
        "createdAt": datetime.now(timezone.utc).isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
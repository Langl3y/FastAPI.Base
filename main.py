from fastapi import FastAPI, APIRouter
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware

from api.routers import tasks_router, users_router, weather_info_router, login_router
from be.env import allowed_hosts

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Include OPTIONS
    allow_headers=["*"],
)

# Include routers


"""
Split routers for api clarity
"""
api_router = APIRouter(prefix='/api')
api_router.include_router(tasks_router)
api_router.include_router(users_router)
api_router.include_router(weather_info_router)
app.include_router(api_router)
app.include_router(login_router)


@app.get("/version")
def main():
    return {"task_management": {
        "version": "1.0.0",
        "author": "hieuhv"
    }}


@app.get('/api')
def api_list():
    return {
            "api": {
                "tasks": [
                    "get_tasks",
                    "create_task",
                    "update_task",
                    "delete_task"
                ],
                "users": [
                    "get_users",
                    "create_user",
                    "update_user",
                    "delete_user"
                ]
            }
        }

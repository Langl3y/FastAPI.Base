from fastapi import FastAPI, APIRouter
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from api.routers import tasks_router, users_router
from be.env import allowed_hosts

app = FastAPI()
app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

# Include routers


"""
Split routers for api clarity
"""
api_router = APIRouter(prefix='/api')
api_router.include_router(tasks_router)
api_router.include_router(users_router)
app.include_router(api_router)


@app.get("/")
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

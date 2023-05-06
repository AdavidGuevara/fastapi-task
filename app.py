from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware
from routes.task_routes import task
from fastapi import FastAPI
import uvicorn

middleware = [Middleware(SessionMiddleware, secret_key="super-secret")]

app = FastAPI(
    title="Lista de tareas",
    description="Un app que almacena las tareas por realizar",
    version="1.0",
    middleware=middleware
)

app.include_router(task)

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)

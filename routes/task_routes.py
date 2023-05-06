from starlette.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Depends, Request, Form, status
from starlette.templating import Jinja2Templates
from conn.connection import SessionLocal
from sqlalchemy.orm import Session
from lib.check import check_title
from models.task import Task
import typing


def flash(request: Request, message: typing.Any, category: str = "") -> None:
    if "_messages" not in request.session:
        request.session["_messages"] = []
    request.session["_messages"].append({"message": message, "category": category})


def get_flashed_messages(request: Request):
    print(request.session)
    return request.session.pop("_messages") if "_messages" in request.session else []


task = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.globals["get_flashed_messages"] = get_flashed_messages


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@task.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    task_list = db.query(Task).all()
    return templates.TemplateResponse(
        "home.html", {"request": request, "task_list": task_list}
    )


@task.post("/add")
def add(
    request: Request,
    title: str = Form(...),
    db: Session = Depends(get_db),
):
    if not check_title(title):
        new_task = Task(title=title)
        db.add(new_task)
        db.commit()
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        flash(request, "La tarea ya se encuentra registrada", "danger")
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@task.get("/update/{task_id}")
def update(
    request: Request,
    task_id: int,
    db: Session = Depends(get_db),
):
    task = db.query(Task).filter(Task.id == task_id).first()
    task.complete = not task.complete
    db.commit()

    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)


@task.get("/delete/{task_id}")
def delete(
    request: Request,
    task_id: int,
    db: Session = Depends(get_db),
):
    task = db.query(Task).filter(Task.id == task_id).first()
    db.delete(task)
    db.commit()

    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

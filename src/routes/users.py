from fastapi import APIRouter, Depends, status, UploadFile, File, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.services.upload_avatar import UploadService
from src.schemas import UserResponse

router = APIRouter(prefix="/users", tags=["users"])
templates = Jinja2Templates(directory='templates')


@router.get("/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_users_me function is a GET endpoint that returns the current user's information.

    :param current_user: User: Get the current user
    :return: A user object that contains the user’s email address
    """
    return current_user


@router.get("/profile", response_class=HTMLResponse)
async def root(request: Request):
    """
    The root function is the main function of this application.
    It returns a TemplateResponse object, which renders the test_form.html template with two variables: request and email.
    The request variable is passed to all templates automatically by Starlette, so we don't need to pass it explicitly here.

    :param request: Request: Get the request object
    :return: A templateresponse object
    """
    return templates.TemplateResponse('test_form.html', {"request": request, "email": None, "text": None})


@router.post("/profile", response_class=HTMLResponse)
async def root(request: Request, email=Form(), text=Form()):
    """
    The root function is the main function of this application.
    It takes in two parameters, email and text, which are both Form objects.
    The root function then prints out the values of these two form objects to the console.
    Finally, it returns a TemplateResponse object that renders test_form.html with three variables: request (the Request object), email (the value of the email parameter), and text (the value of the text parameter).

    :param request: Request: Access the request object
    :param email: Store the value of the email input field
    :param text: Pass the text to the template
    :return: A templateresponse, which is a special type of response
    """
    print(email, text)
    return templates.TemplateResponse('test_form.html', {"request": request, "email": email, "text": text})


@router.patch('/avatar', response_model=UserResponse)
async def update_avatar_user(avatar: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
    The update_avatar_user function updates the avatar of a user.

    :param avatar: UploadFile: Get the file from the request
    :param current_user: User: Get the current user
    :param db: Session: Access the database
    :return: A user object
    """
    public_id = UploadService.create_name_avatar(current_user.email, 'web10')

    r = UploadService.upload(avatar.file, public_id)

    src_url = UploadService.get_url_avatar(public_id, r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user

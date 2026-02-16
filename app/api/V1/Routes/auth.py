from fastapi  import APIRouter , HTTPException , status , Depends, Path , Query , Cookie,Header , BackgroundTasks , Form , UploadFile
from app import TOKEN_DEPS,GET_SUPER_USER,Current_active_user,SESSION_Dependecy #type:ignore
from fastapi import Request
# from app import UserPublic,UserInDb,UserIn #type:ignore
from app.crud.User_Crud  import usercruds  #type:ignore
# from app.api.deps import GET_SUPER_USER
from typing  import Annotated
from fastapi import Response
from app.models.all_models import MovieIn , MovieOut , Movie , MovieUpdate  , UserIn , UserInDb , UserPublic   #type:ignore
from fastapi.security import OAuth2PasswordRequestForm 
from app.api.deps  import  Get_current_active_SuperUser  , GET_ACCESS_TOKEN_USING_REFRESH_TOKEN #type:ignore
import uuid

router:APIRouter= APIRouter()


@router.post("/sign_up")
def User_Registration(user_data:UserIn , response :Response,  session:SESSION_Dependecy):
    # return user_data
    respnse=usercruds.USER_sign_up(user_data , session ,response )
    return respnse

@router.post("/login/access_token")
def log_in_user(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],session:SESSION_Dependecy):
    
    res=usercruds.user_Login(form_data.username , form_data.password,session)
    return res

@router.post("/get-access-token/refresh-token")
def get_access_token_by_refreshToken(access_token :GET_ACCESS_TOKEN_USING_REFRESH_TOKEN ,session:SESSION_Dependecy):
    
    if access_token:
        return {"status":status.HTTP_200_OK,"access_token":access_token}   
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
import datetime

router:APIRouter= APIRouter()


@router.get("/get-all-users")
def GellAllUsers(superUser:GET_SUPER_USER,session:SESSION_Dependecy):
    res=usercruds.get_all_users(session)
    return res

@router.delete("/delete-specific-user/user/{user_id}" , dependencies=[Depends(Get_current_active_SuperUser)])
def delete_user_by_id(*,user_id:str=Path() , session:SESSION_Dependecy):
    try:
       user:UserInDb|None=session.get(UserInDb , user_id)
       if not user:
           raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="User not found"
           )
           
       user.is_deleted=True
       user.deleted_at=datetime.datetime.now(datetime.timezone.utc)
       session.add(user)
       session.commit()
        
    except HTTPException :
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error "
        )    
    
    

    
@router.post("/add-movie")
def AddMovie(*,movie_data:Annotated[ MovieIn,Form()] ,movie_trailor:UploadFile| None=None , poster_file:UploadFile|None=None , backdrop_file:UploadFile|None=None ,super_user:GET_SUPER_USER, session:SESSION_Dependecy):
    res= usercruds.add_movie(movie_data , movie_trailor , poster_file , backdrop_file , session)
    


@router.patch("/update-movie/{movie_id}" , dependencies=[Depends(Get_current_active_SuperUser)])
def UpdateMovie(movie_id:Annotated[str,Path(...,gt=0)] , movie_data:MovieUpdate ,session:SESSION_Dependecy)->MovieOut:
    movie_id_uuid:uuid.UUID=uuid.UUID(movie_id)
    res=usercruds.update_movie(movie_id_uuid , movie_data , session)
    return res

@router.post("/add-poster/{movie_id}" ,dependencies=[Depends(Get_current_active_SuperUser)])
def AddposterToMOvie(movie_id:Annotated[str , Path(...,gt=0)] , poster_file:UploadFile , session:SESSION_Dependecy)->dict[str,str]:
    movie_id_uuid:uuid.UUID=uuid.UUID(movie_id)
    res = usercruds.add_poster_to_movie(movie_id_uuid , poster_file , session)
    return res
@router.post("/add-backdrop/{movie_id}" ,dependencies=[Depends(Get_current_active_SuperUser)])
def AddBackdropToMOvie(movie_id:Annotated[str , Path(...,gt=0)] , backdrop_file:UploadFile , session:SESSION_Dependecy)->dict[str,str]:
    movie_id_uuid:uuid.UUID=uuid.UUID(movie_id)
    res = usercruds.add_backdrop_to_movie(movie_id_uuid , backdrop_file , session)
    return res


@router.delete("/delete-movie/{movie_id}" , dependencies=[Depends(Get_current_active_SuperUser)])
def delete_movie(movie_id:Annotated[str , Path(...,gt=0)] ,session:SESSION_Dependecy)->dict[str,str]:
    movie_id_uuid:uuid.UUID=uuid.UUID(movie_id)
    res=usercruds.delete_movie(movie_id_uuid , session)
    return res

@router.get("/get-all-active-users" , dependencies=[Depends(Get_current_active_SuperUser)])
def get_all_active_users(session:SESSION_Dependecy):
    res=usercruds.get_all_active_users(session)
    return res
@router.get("/get-all-deleted-users" , dependencies=[Depends(Get_current_active_SuperUser)])
def get_all_deleted_user(session:SESSION_Dependecy):
    res  = usercruds.get_all_deleted_users(session)

@router.get("/get-all-customers",dependencies=[Depends(Get_current_active_SuperUser)])
def get_all_customers(session:SESSION_Dependecy):
    return usercruds.get_all_customers(session)

@router.get("/get-all-threators_managers" , dependencies=[Depends(Get_current_active_SuperUser)])
def get_all_therators_managers(session:SESSION_Dependecy):
    return usercruds.get_all_threators_managers(session)





from sqlmodel  import Session , select
import sqlalchemy
from fastapi import HTTPException , status
from app.core.settings  import setting #type:ignore
from app.models.UserModel  import payload_Token  #type:ignore
from app.models.refresh_model import UserRefreshToken #type:ignore
from app import verify_hashed_password , get_password_hash , Create_access_token , Create_RefreshToken #type:ignore
from datetime import datetime , timedelta , timezone
from app.models.all_models  import UserInDb , UserIn   #type:ignore
from app.models.all_models import MovieIn , MovieOut , Movie  , MovieUpdate
from pathlib import Path
from fastapi import UploadFile , Response
import os
import uuid 
from datetime import datetime , timedelta , timezone
import shutil
class  UsersCrud():
    
    def __check_user_exist(self,username:str , email:str,session:Session ):
        # print("Hello g ")
        # return  1 , 2 
        user:UserInDb|None=session.exec(select(UserInDb).where(UserInDb.username==username)).one_or_none()
        # print('HelloBG Is ',user)
        # return 
        if not user :
            user_e:UserInDb|None=session.exec(select(UserInDb).where(UserInDb.email==email)).one_or_none()
            if not user_e:
                return False , "ok"
            else:
                return True , "email_exist"
        else :    
           return True  ,"username_exist"  # True means user exist with username or email
    
    def USER_sign_up(self,user:UserIn, session:Session , response :Response):
        
        try:
            # return 
            exist_bool,exist_str=self.__check_user_exist(user.username , user.email,session)
            # return "hello"
            if not exist_bool and exist_str =="ok":
                #  createing New User in DB
                R_User:UserInDb=UserInDb.model_validate( 
                  user , update={"hashed_password":get_password_hash(user.password)}  
                )
                session.add(R_User)
                session.commit()
                
                session.refresh(R_User)
                # print(type(R_User.id))
                
                expire_acess_token_Time=setting.Expire_ACCESS_TOKEN
                expire_refresh_token_time=setting.Expire_Refresh_TOKEN
                data={
                    "id":str(R_User.id),
                    "username":R_User.username,
                    "email":R_User.email
                }  
                
                PayloadAndToken:payload_Token=payload_Token(
                    id=R_User.id,
                    username=R_User.username,
                    email=R_User.email,
                    is_active= not R_User.is_deleted,
                    role=R_User.role,
                    access_token=Create_access_token(data,timedelta(hours=expire_acess_token_Time)),
                    re_fresh_token=Create_RefreshToken(data , timedelta(days=expire_refresh_token_time))
                    
                 ) 
                
                jti:str=PayloadAndToken.re_fresh_token["jti"]
                
                refreshTokenMOdel=UserRefreshToken(
                    jti=jti,
                    user=R_User
                )
                session.add(refreshTokenMOdel)
                session.commit()
                session.refresh(refreshTokenMOdel)
                
                # response.set_cookie(
                #     key="access_token",
                #     value=PayloadAndToken.access_token,
                #     httponly=True,
                #     secure= False,
                    
                # )
                
                
                
                return PayloadAndToken
            elif exist_bool and (exist_str == "email_exist" or exist_str == "username_exist"):
            # This will now be caught by FastAPI instead of your 'except' block below
                raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A user with this {'email' if exist_str == 'email_exist' else 'username'} already exists."
                 )

        except HTTPException:
        # Re-raise the HTTPException so it doesn't get caught by the generic Exception block
            raise
        except Exception as e:
                    # Log the real error to your console so you can debug it!
            print(f"DEBUG: Real error was: {e}") 
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something unexpected happened"
            )
        
    def __Authenticate_user(self,username:str,password:str,session:Session)->UserInDb:
       ...
       user:UserInDb |None = session.exec(select(UserInDb).where(UserInDb.username==username)).one_or_none() 
       if not user:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                               detail="UserName is incorrect. User not found!")
       
       if not verify_hashed_password(password , user.Hashed_Password):
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                               detail="Invalid username and Password") 
       return user               
            
    def user_Login(self , username:str,passoword:str , session:Session):
        ...
        # return {"user":username,"pass":passoword}
        user:UserInDb=self.__Authenticate_user(username,passoword,session)
        # return user
        userOldRefreshToken:UserRefreshToken|None=session.exec(select(UserRefreshToken).where(UserRefreshToken.userId==user.id)).one_or_none()
        # return userOldRefreshToken
        if userOldRefreshToken:
            # return "Hello g "
            if user:
                expire_acess_token_Time=setting.Expire_ACCESS_TOKEN
                expire_refresh_token_time=setting.Expire_Refresh_TOKEN
                    
                data={
                    "id":user.id,
                    "username":user.username,
                    "email":user.email
                }  
                refresh_token=Create_RefreshToken(data , timedelta(days=expire_refresh_token_time))
                jti:str=refresh_token["jti"]
                
                PayloadAndToken:payload_Token=payload_Token(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    is_active=user.is_active,
                    is_super_user=user.is_super_user,
                    access_token=Create_access_token(data,timedelta(minutes=expire_acess_token_Time)),
                    re_fresh_token={"refresh_token":refresh_token["refresh_token"]}
                    ) 
                userOldRefreshToken.jti=jti
                session.add(userOldRefreshToken)
                session.commit()
                session.refresh(userOldRefreshToken)
                return PayloadAndToken
                
    def refill_balance(self , user:UserInDb , amount:int , session:Session):
        ...
        try:
            # user:UserInDb|None=session.get(UserInDb , currentuser.id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User Not Found"
                )
            user.balance += amount
            session.add(user)
            session.commit()
            session.refresh(user)
            return {"balance":user.balance}
        except HTTPException:
            raise
        except Exception as e:
            print(f"DEBUG: Real error was: {e}") 
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something unexpected happened while refilling balance"
            )
            
    # def add_movie(self,trailor_file,poster_file , backdrop_file , session:Session):
    def add_movie(self,movie_data:MovieIn,trailor_file,poster_file , backdrop_file , session:Session):
        
        try:
            
            
            corefilder= Path("Movies_Details")
            foldername=movie_data.title
            movieFolder=corefilder/foldername
            movieFolder.mkdir(exist_ok=True , parents=True)
            # return "Hello"
            if trailor_file:
                ext_is=Path(trailor_file.filename).suffix
                movie_trailor_path=Path(movieFolder/f"{trailor_file.filename}")
                with open(movie_trailor_path , "wb") as buffer:
                    shutil.copyfileobj(trailor_file.file , buffer)
            
            if poster_file:
                ext_is=Path(poster_file.filename).suffix
                
                posterFolder=Path(movieFolder/f"poster")
                posterFolder.mkdir(exist_ok=True)   
                
                movie_poster_path=Path(posterFolder/f"{poster_file.filename}")
                with open(movie_poster_path , "wb") as buffer:
                    shutil.copyfileobj(poster_file.file , buffer)
            
            if backdrop_file:
                ext_is=Path(backdrop_file.filename).suffix
                
                backdropFolder=Path(movieFolder/f"backdrop")
                backdropFolder.mkdir(exist_ok=True)
                
                backdrop_pathIs=Path(backdropFolder/f"{backdrop_file.filename}")
                with open(backdrop_pathIs , "wb") as buffer:
                    shutil.copyfileobj(backdrop_file.file , buffer)
                  
            MOviedata=Movie.model_validate(
                movie_data , update={
                    "trailor_path":str(movie_trailor_path) if trailor_file else str(movieFolder),
                    "poster_path":str(movie_poster_path) if poster_file else str(f"{movieFolder}/poster"),
                   "backdrop_path":str(backdrop_pathIs) if backdrop_file else str(f"{movieFolder}/backdrop")
                }
            )
            
            
            session.add(MOviedata)
            session.commit()
            session.refresh(MOviedata)
            return MOviedata
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while saving movie files."
            )
        
        
    def update_movie(self ,movie_id:uuid.UUID,movie_data:MovieUpdate, session:Session):
        ...
        try:
            
            movie:Movie=session.get(Movie,movie_id)
            if not movie:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Movie Not Found"
                )  
            movie_data_dict:dict=movie_data.model_dump(exclude_unset=True)
            
            movie.sqlmodel_update(movie_data_dict )
            session.add(movie)
            session.commit()
            session.refresh(movie)
            return movie
                 
            
        except Exception as e:
            raise HTTPException(
                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                 detail="Something is unexpected heppen at update movie"
            )    
    
    def add_poster_to_movie(self , movie_id:uuid.UUID , poster_file:UploadFile , session:Session):
        try:
            movie:Movie=session.get(Movie,movie_id)
            if not movie:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Movie Not Found"
                )  
            ext_is=Path(poster_file.filename).suffix  #type:ignore
            
            # movieFolder=Path("Movies_Details")/movie.title
            poster_url:str=movie.poster_url
                
            # posterFolder=Path(movieFolder/f"poster")
            # posterFolder.mkdir(exist_ok=True)   
                
            movie_poster_path=Path(poster_url/f"{poster_file.filename}") #type:ignore
            with open(movie_poster_path , "wb") as buffer:
                shutil.copyfileobj(poster_file.file , buffer)
            
            movie.poster_url=str(movie_poster_path)
            session.add(movie)
            session.commit()
            # session.refresh(movie)
            return {"movie_id":movie_id,"poster_url":str(movie_poster_path)}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while saving movie poster."
            )
    def add_backdrop_image_to_movie(self , movie_id:uuid.UUID , backdrop_file:UploadFile , session:Session):
        try:
            movie:Movie=session.get(Movie,movie_id)
            if not movie:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Movie Not Found"
                )  
            ext_is=Path(backdrop_file.filename).suffix  #type:ignore
            
            # movieFolder=Path("Movies_Details")/movie.title
            backdrop_url:str=movie.backdrop_url                             
                
            # backdropFolder=Path(movieFolder/f"backdrop")
            # backdropFolder.mkdir(exist_ok=True)   
                
            movie_backdrop_path=Path(backdrop_url/f"{backdrop_file.filename}")    #type:ignore
            with open(movie_backdrop_path , "wb") as buffer:
                shutil.copyfileobj(backdrop_file.file , buffer)
            
            movie.backdrop_url=str(movie_backdrop_path)
            session.add(movie)
            session.commit()
            # session.refresh(movie)
            return {"movie_id":movie_id , "backdrop_url":str(movie_backdrop_path)}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while saving movie poster."
            )
    
    
    def delete_movie(self , movie_id:uuid.UUID , session:Session):
        ...
        try:
            movie:Movie=session.get(Movie,movie_id)
            if not movie:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Movie Not Found"
                )
            
            utc_time_now=datetime.now(timezone.utc)
            movie.is_deleted=True
            movie.deleted_at=utc_time_now
            session.add(movie)
            session.commit()
            return {"movie_id":movie_id , "msg":f"Movie with id {movie_id}  Deleted Successfully"}
                  
        #     session.delete(movie)
        #     session.commit()
        #     return {"message":"Movie Deleted Successfully"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while deleting movie."
            )
    def get_all_users(self,session:Session):
        
        all_users=session.exec(select(UserInDb)).all()
        return all_users 

    def get_all_active_users(self , session:Session):
        
        active_Users:UserInDb=session.exec(select(UserInDb).where(UserInDb.is_deleted==False)).all()
        return active_Users
    
    def get_all_deleted_users(self , session:Session):
        
        deleted_Users:UserInDb=session.exec(select(UserInDb).where(UserInDb.is_deleted==True)).all()
        return deleted_Users
    
    def get_all_customers(self , session:Session):
        
        customers:UserInDb=session.exec(select(UserInDb).where(UserInDb.role=="customer")).all()
        return customers
    
    def get_all_threators_managers(self , session:Session):
        
        threators:UserInDb=session.exec(select(UserInDb).where(UserInDb.role=="theater_manager")).all()
        return threators
    
    


usercruds=UsersCrud()            
        
        
        
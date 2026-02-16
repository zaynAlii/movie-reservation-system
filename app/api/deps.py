from fastapi import HTTPException , status , Depends
from fastapi.security import OAuth2PasswordBearer
from ..core import engine
from sqlmodel import Session
import jwt
# from pydantic.errors import in
from jwt.exceptions  import InvalidTokenError , ExpiredSignatureError , PyJWTError 
from ..core import setting
from ..models import Payload
from ..models.all_models import UserInDb
from typing import Annotated
from app.models.UserModel  import Decode_token_payload  #type:ignore
from uuid import UUID
from app.core.security import Create_access_token  #type:ignore
from datetime import datetime   , timedelta
auth_Schema=OAuth2PasswordBearer(tokenUrl="api/V1/login/access_token")



TOKEN_DEPS=Annotated[str,Depends(auth_Schema)]

async def getSession():
    try:
        with Session(engine) as session:
            yield session
    except HTTPException:
        raise        
    except Exception as e:
        raise e
        # raise HTTPException(
        #     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #     detail="This error occureed while creating session with postgess db "
        # ) from e
        

SESSION_Dependecy=Annotated[Session, Depends(getSession)]        
        


def Get_currentUser(token:TOKEN_DEPS,session:SESSION_Dependecy ) :
    credential_Exception=HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
             detail="Could not validate Credentials ",
            headers={"WWW-Authenticate":"Bearer"}
        )
    
    try:
        ...
        # print(token)
        print(setting.secret_key , setting.algorithm)
        # print("Hello_1")
        payload_data= jwt.decode(token ,setting.secret_key ,algorithms=[setting.algorithm] )
        # print("Hello_2")

        payload:Decode_token_payload=Decode_token_payload.model_validate(payload_data)
        # print("Hello_3")
        # payloadDict:dict[str,str|int]=payloadModel.model_dump()
        if not payload.id or not payload.username:
            raise credential_Exception
        # print("Hello")
        try:
            user_id = UUID(payload.id)
        except (ValueError , TypeError):
            raise credential_Exception
        UserIs:UserInDb|None = session.get(UserInDb ,user_id)
        # print("Hello")
        if not UserIs:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User Not Found"
            )            
        
        if  UserIs.is_deleted:
            raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"User {UserIs.username} is inactive. Please contact support or verify your email."
                )
        
        return UserIs
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been expired, Please LogIn Again"
        )    
               
        
    except (InvalidTokenError ) :
        raise credential_Exception
    
Current_active_user=Annotated[UserInDb , Depends(Get_currentUser)]



def verify_refresh_Token(token:TOKEN_DEPS , session:SESSION_Dependecy):
    credential_Exception=HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
             detail="Could not validate Credentials ",
            headers={"WWW-Authenticate":"Bearer"}
        )
    
    try:
        
        payload_data=jwt.decode(token , setting.secret_key ,algorithms=[setting.algorithm])
        payload_model:Decode_token_payload = Decode_token_payload.model_validate(payload_data)
        
        if not payload_model.id or not payload_model.username:
            raise credential_Exception
        
        try:
            user_id:UUID=UUID(payload_model.id)
        except (ValueError , TypeError):
            raise credential_Exception
        
        User_is:UserInDb|None=session.get(UserInDb , user_id)
        if not User_is:
            raise     HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User Not Found"
            )
        if User_is.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User {User_is.username} is inactive. Please contact support or verify your email."
            )    
        
        if payload_model.type == "refresh":
            jti=payload_model.jti
            
            if not User_is.haveRefreshToken:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"No active refresh token found for user"
                )
            
            user_jti_in_db=User_is.haveRefreshToken.jti
            
            if jti == user_jti_in_db :
                
                access_token_expired_time=setting.Expire_ACCESS_TOKEN
                
                user_data_to_encode:dict[str , str|int] = {
                    "id":payload_model.id,
                    "username":payload_model.username,
                    "email":payload_model.email
                }
                
                user_acceess_token_is=Create_access_token(user_data_to_encode , timedelta(hours=access_token_expired_time))
                return user_acceess_token_is         
            
            else :
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Refresh token(token mis_matched)"
                )
            
            
        elif payload_model.type =="access":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST , 
                detail=f"you cant get an access token using an access token .  use a refresh token"
            )    
    
    
    
    except  ExpiredSignatureError:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been expired, Please LogIn Again"
        )    
         
           
    except (InvalidTokenError , Exception ) :
        raise  credential_Exception 
    
GET_ACCESS_TOKEN_USING_REFRESH_TOKEN=Annotated[dict[str ,str] , Depends(verify_refresh_Token)]    
    
def Get_current_active_SuperUser(superUser:Current_active_user):
    if not superUser.role =="admin":
        raise   HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have enogh priviliges",
            headers={"WWW-Authenticate":"Bearer"}
            )
    return superUser    


GET_SUPER_USER=Annotated[UserInDb , Depends(Get_current_active_SuperUser)]


def get_current_threater_manager(threator_manager:Current_active_user):
    if not threator_manager.role == "theater_manager":
        raise   HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have enogh priviliges",
            headers={"WWW-Authenticate":"Bearer"}
            )
        
    return threator_manager


GET_THREATOR_MANAGER=Annotated[UserInDb ,Depends(get_current_threater_manager)]

def verify_superUser(session:SESSION_Dependecy , user_id:int):
    
    user:UserInDb|None=session.get(UserInDb, user_id)  
    if not user:
        raise  HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User Not Found"
            )  
    
    if  user.is_deleted:
        raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Inactive user. Please contact support or verify your email."
                )     
         
    if not user.role =="admin":
         raise   HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have enogh priviliges"
            )
         
    return user     



    
    
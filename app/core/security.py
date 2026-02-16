import jwt
from datetime import datetime  , timedelta , timezone
from app.core.settings import setting #type:ignore
import uuid


from pwdlib import PasswordHash


password_Helper=PasswordHash.recommended()



def get_password_hash(password:str):
    return password_Helper.hash(password)


def verify_hashed_password(password:str, hashpassword:str):
    return password_Helper.verify(password,hashpassword)


def Create_access_token(data:dict[str,str|int],expires:timedelta|None=None):
    # return "kmkmskdmksmdkmdks"
    to_encode:dict[str, str|int]=data.copy()
    # return to_encode
    # jti:str=str(uuid.uuid4())
    if expires :
        expires_At:datetime=datetime.now(timezone.utc) + expires   
        
    else:
        expires_At:datetime=datetime.now(timezone.utc) + timedelta(minutes=20)  #type:ignore 
    
    to_encode.update({"exp":expires_At,"type": "access" }) #type:ignore
    print(to_encode)
    return jwt.encode(to_encode, setting.secret_key , setting.algorithm)
    

def Create_RefreshToken(userdata:dict[str,str|int], expireTime:timedelta|None=None):
    to_encode=userdata.copy()
    jti:str=str(uuid.uuid4())
    
    if expireTime:
        expires_at:datetime=datetime.now(timezone.utc) + expireTime
    else:
        expires_at:datetime=datetime.now(timezone.utc) + timedelta(days=7)   #type:ignore
    
    to_encode.update({"exp":expires_at,"type": "refresh","jti":jti})  #type:ignore
    
    return {"jti":jti,
            "refresh_token":jwt.encode(to_encode,setting.secret_key , setting.algorithm)
            }

 
    
    
    
    
    
    
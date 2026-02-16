from sqlmodel import create_engine
from app.core.settings import setting  #type:ignore

   

# connection_Str=setting.Database_Url

# print(connection_Str)

connection_Str:str=setting.Database_Url.replace(
    "postgresql", "postgresql+psycopg"
)
# print(connection_Str)

engine=create_engine(connection_Str,echo=True)


from pydantic_settings import BaseSettings , SettingsConfigDict
class Settings(BaseSettings):
    model_config=SettingsConfigDict(
        env_file=".env" , env_ignore_empty=True, extra="ignore"
    )
    secret_key:str
    Database_Url:str 
    algorithm:str
    Expire_ACCESS_TOKEN:int   #  #mints
    Expire_Refresh_TOKEN:int


setting=Settings()  #type:ignore
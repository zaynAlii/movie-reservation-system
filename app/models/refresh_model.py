from sqlmodel import SQLModel , Field , Relationship
from app.models.all_models import UserInDb  #type:ignore
from  typing import Annotated
import datetime
from sqlalchemy.dialects.postgresql  import UUID  as PG_UUID
from sqlalchemy import Column
import uuid
class UserRefreshToken(SQLModel ,table=True):
    __tablename__ = "userrefreshtoken"
    id:uuid.UUID=Field(
                  default_factory=uuid.uuid4 ,
                  sa_column=Column(PG_UUID(as_uuid=True) , primary_key=True))
    jti:Annotated[str,Field(unique=True)]
    userId:uuid.UUID= Field(foreign_key="users.id" , index=True)
    expires_at: datetime.datetime | None = Field(default=None)

    user:'UserInDb'=Relationship(
        back_populates="haveRefreshToken"
    )   
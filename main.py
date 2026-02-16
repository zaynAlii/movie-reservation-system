import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# from app.core.settings import setting
from sqlmodel import SQLModel
from app import   setting , engine  #type:ignore
from app.models import all_models  #type:ignore
from contextlib  import asynccontextmanager
# from app.core.db_settings import engine  #type:ignore
from fastapi.responses  import RedirectResponse
from fastapi  import FastAPI
from app.api.V1.connect  import connect_router   #type:ignore
from fastapi.staticfiles  import StaticFiles

from starlette.middleware.cors  import CORSMiddleware
def create_Tables():
    # Creating  The Table
    SQLModel.metadata.create_all(engine)
@asynccontextmanager
async def lifespan(app:FastAPI):
#    create_Tables()
   yield
   
app:FastAPI = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/get_static_files" , StaticFiles(directory="Movies_Details/") , name="static_route")

app.include_router(connect_router,prefix="/api/V1")


@app.get("/")
def ToDocs()->RedirectResponse:
    return RedirectResponse(url="/docs")




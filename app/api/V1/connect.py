from fastapi  import APIRouter
from app.api.V1.Routes  import user #type:ignore
from app.api.V1.Routes import threator_manager
from app.api.V1.Routes import customer
from app.api.V1.Routes import auth
connect_router=APIRouter()
connect_router.include_router(auth.router,prefix="/auth",tags=["Auth"])
connect_router.include_router(user.router,prefix="/admin",tags=["Admin"])
connect_router.include_router(threator_manager.router,prefix="/threator_manager",tags=["Threator_Manager"])
connect_router.include_router(customer.router,prefix="/customer",tags=["Customer"])
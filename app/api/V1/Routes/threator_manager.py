from fastapi  import APIRouter , Depends , HTTPException , status  , Path
from app.models.all_models  import  ThreaterCreate , ThreaterUpdate , Theater , ThreatorOut  #type:ignore
from app.api.deps  import SESSION_Dependecy , GET_THREATOR_MANAGER , get_current_threater_manager #type:ignore
from app.crud.threator_manager_crud  import threator_cruds #type:ignore
from fastapi import Query
import uuid
from app.models.all_models  import (Screen , ScreenCreate ,ScreenOut , ScreenType ,ScreenUpdate,
                                    Seat , SeatCreate , SeatOut , SeatType
                                    ,ShowtimeCreate , Showtime , ShowTimeOut , ShowtimeStatus ,ShowtimeUpdate
                                    
                                    
                                    )
from typing import Annotated
router=APIRouter()



@router.post("/register-threator")
def register_threator(threator_data:ThreaterCreate, threator_manager:GET_THREATOR_MANAGER,session:SESSION_Dependecy ):
    # return threator_manager
    return threator_cruds.register_threater(threater_data=threator_data , threator_manager=threator_manager ,session=session)

@router.patch("/theater-update/{theater_id}",dependencies=[Depends(get_current_threater_manager)])
def update_theater(theater_to_update:ThreaterUpdate ,theater_id:str , session:SESSION_Dependecy):
    theater_id_uuid:uuid.UUID=uuid.UUID(theater_id)
    return     threator_cruds.update_threater(data_to_update=theater_to_update , threator_ud=theater_id_uuid , session=session)


@router.delete("/delete-theater/{theater_id}", dependencies=[Depends(get_current_threater_manager)])
def theater_to_delete(theater_id:Annotated[str , Path(...)] , session:SESSION_Dependecy)   :
    
    theater_id_uuid:uuid.UUID=uuid.UUID(theater_id)
    return threator_cruds.theater_to_deleted(theater_id=theater_id_uuid , session=session)
    
@router.post("/add-screen-to-theater/{theater_id}", dependencies=[Depends(get_current_threater_manager)])
def add_screen_to_theater(theater_id:Annotated[str,Path(...)],screen_data:ScreenCreate,session:SESSION_Dependecy):
    theater_id_uuid:uuid.UUID=uuid.UUID(theater_id)
    return threator_cruds.screen_to_be_added_to_theater(theater_id_uuid , screen_data,session)

@router.patch("/update-screen/{screen_id}" , dependencies=[Depends(get_current_threater_manager)])
def screen_tobeupdated(screen_id:Annotated[str , Path(...)] ,update_screen:ScreenUpdate ,session:SESSION_Dependecy):
    
    screen_id_uuid:uuid.UUID=uuid.UUID(screen_id)
    
    return threator_cruds.screen_to_be_updated(screen_id_uuid ,update_screen ,session)

@router.delete("/delete-screen/{screen_id}" , dependencies=[Depends(get_current_threater_manager)])
def delete_screen(screen_id:Annotated[str , Path(...)]  ,session:SESSION_Dependecy):
    
    screen_id_uuid:uuid.UUID=uuid.UUID(screen_id)
    
    return threator_cruds.screen_to_be_deleted(screen_id_uuid  ,session)

@router.post("/add-seat-screen/{screen_id}" ,dependencies=[Depends(get_current_threater_manager)])
def add_seattoscreen(screen_id:Annotated[str , Path(...)] ,seat_data:SeatCreate ,session:SESSION_Dependecy):
    
    screen_id_uuid:uuid.UUID=uuid.UUID(screen_id)
    
    return threator_cruds.add_seat(screen_id_uuid , seat_data , session)


@router.post("/make-seat-deactive/screen/{screen_id}/seat/{seat_id}" , dependencies=[Depends(get_current_threater_manager)])
def make_seatdeactive(screen_id:Annotated[str  , Path(...)] ,seat_id:Annotated[str  , Path(...)] ,session:SESSION_Dependecy):
    
    screen_id_uuid:uuid.UUID=uuid.UUID(screen_id)
    seat_id_uuid:uuid.UUID=uuid.UUID(seat_id)
    
    return threator_cruds.make_seat_deactive(screen_id , seat_id,session)


@router.post("/make-seat-active/screen/{screen_id}/seat/{seat_id}" , dependencies=[Depends(get_current_threater_manager)])
def make_seatactive(screen_id:Annotated[str  , Path(...)] ,seat_id:Annotated[str  , Path(...)] ,session:SESSION_Dependecy):
    
    screen_id_uuid:uuid.UUID=uuid.UUID(screen_id)
    seat_id_uuid:uuid.UUID=uuid.UUID(seat_id)
    
    return threator_cruds.make_seat_active(seat_id,session)



@router.delete("/delete-seat/seat/{seat_id}" , dependencies=[Depends(get_current_threater_manager)])
def delete_seat(seat_id:Annotated[str  , Path(...)] ,session:SESSION_Dependecy):
    
    # screen_id_uuid:uuid.UUID=uuid.UUID(screen_id)
    seat_id_uuid:uuid.UUID=uuid.UUID(seat_id)
    
    return threator_cruds.delete_seat(seat_id,session)


@router.post("/creare-showtime/screen/{screen_id}/movie/{movie_id}" , dependencies=[Depends(get_current_threater_manager)])
def create_showtimee(screen_id:Annotated[str , Path(...)],movie_id:Annotated[str , Path(...)]  ,showtime_data:ShowtimeCreate , session:SESSION_Dependecy):
    return threator_cruds.create_showtime(showtime_data , screen_id , movie_id , session)


@router.post("/mark_showtime_cancel/showtime{showtime_id}" , dependencies=[Depends(get_current_threater_manager)])
def cancel_showtime(showtime_id:Annotated[str, Path(...)], session:SESSION_Dependecy):
    return threator_cruds.mark_showtime_to_cancelled(showtime_id , ShowtimeStatus.CANCELLED , session)




@router.post("/update-showtime/{showtime_id}" , dependencies=[Depends(get_current_threater_manager)])
def showtime_update(showtime_id:Annotated[str  ,Path(...) ] ,showtime_update_data:ShowtimeUpdate, session:SESSION_Dependecy):
    return threator_cruds.update_Showtime(showtime_id , showtime_update_data , session)


@router.get("/theater-details")
def get_Threater_deatils(manager:GET_THREATOR_MANAGER,sesion:SESSION_Dependecy):
    return threator_cruds.get_theater_info(manager, sesion)



@router.get("/get-screen-seats/screen/{screen_id}" , dependencies=[Depends(get_current_threater_manager)])
def get_screen_seats(screen_id:Annotated[str , Path(...)], session:SESSION_Dependecy):
    screen_id_uuid:uuid.UUID=uuid.UUID(screen_id)
    return threator_cruds.get_screen_seats(screen_id_uuid , session)




@router.get("/see-showtime-seats-status/showtime/{showtime_id}" , dependencies=[Depends(get_current_threater_manager)])
def get_showtime_all_seat_status(showtime_id:Annotated[str , Path(...)], session:SESSION_Dependecy):
    showtime_id_uuid:uuid.UUID=uuid.UUID(showtime_id)
    return threator_cruds.see_showtime_seats(showtime_id_uuid , session)


@router.get("/get-all-showtimes-by-theater/{theater_id}")
def get_all_showtimes_by_theater(manager:GET_THREATOR_MANAGER,session:SESSION_Dependecy,active:bool|None=False ):
    theater_id_uuid:uuid.UUID=uuid.UUID(manager.haveThreator.id)
    return threator_cruds.get_all_showtimes_info(theater_id_uuid , session , active)



@router.get("/get-showtimes-booking-details/showtime/{showtime_id}" , dependencies=[Depends(get_current_threater_manager)])
def get_showtimes_booking_details(showtime_id:Annotated[str , Path(...)], session:SESSION_Dependecy):
    showtime_id_uuid:uuid.UUID=uuid.UUID(showtime_id)
    return threator_cruds.get_all_booking_showtime(showtime_id_uuid , session)

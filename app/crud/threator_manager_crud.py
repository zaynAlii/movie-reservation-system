from fastapi import  HTTPException , status ,Depends
from sqlmodel  import Session , select
from app.models.all_models import UserInDb , ThreaterCreate , ThreaterUpdate , ThreatorOut,Theater  #type:ignore
import uuid
import datetime
from typing import Any
import random
# from sqlalchemy.orm import in 
import string
from app.models.all_models import (
                           Screen , ScreenCreate ,ScreenOut ,
                           ScreenUpdate , Seat , SeatType ,
                           SeatCreate , SeatOut,
                           Showtime,ShowtimeCreate,ShowtimeStatus,ShowTimeOut,
                           Movie , ShowtimeUpdate , Booking, BookingStatus , 
                           BookingCreateTimingStatus , Payment,PaymentStatus,
                           PaymentMethod
                           )
class  TheraterCruds():
    def register_threater(self,threater_data:ThreaterCreate ,threator_manager:UserInDb ,session:Session ):
        try:
            ...
            threator_is:Theater=Theater.model_validate(threater_data)
            
            threator_manager.haveThreator=threator_is
            
            session.add(threator_manager)
            session.commit()
            session.refresh(threator_is)
            return threator_is
            
            
        except Exception as e:
            print(f"Actual Error Is :====", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpcted thing heppend in server"
            )
    def update_threater(self,data_to_update:ThreaterUpdate,threator_ud:uuid.UUID ,session:Session):
        ...        
        try:
            Threater:Theater|None=session.get(Theater,threator_ud)
            if not Threater:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"The Threater with id {threator_ud} not found"
                )
            
            data_to_update_dict=data_to_update.model_dump(exclude_unset=True)
            
            Threater.sqlmodel_update(data_to_update_dict)
            
            session.add(Threater)
            session.commit()
            session.refresh(Threater)
        except HTTPException :
            raise                        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected thing Hppened hehe  nalla develeper! 😂"
            )    
    def theater_to_deleted(self,theater_id:uuid.UUID , session:Session):
        try:
            theater_is:Theater|None=session.get(Theater , theater_id)
            if not theater_is:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Theater with id {theater_id } not found"
                )
            
            theater_is.is_deleted=True
            theater_is.deleted_at=datetime.datetime.now(datetime.timezone.utc)
            session.add(theater_is)
            session.commit()
            return {"status":status.HTTP_202_ACCEPTED,"theater_id":theater_id,"message":"Theater Deleted Successfully"}    
        except HTTPException :
            raise;        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected thing happen in deleteting the theater with id {theater_id} "
            )            
            
    def screen_to_be_added_to_theater(self, theater_id:uuid.UUID ,screen_data:ScreenCreate, session:Session):
        try:
            theater_Is:Theater|None=session.get(Theater , theater_id)
            if not theater_Is:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Theater with id {theater_id} not found"
                )
            
            Screen_to_be_added:Screen=Screen.model_validate(screen_data)
            
            capacity:int=Screen_to_be_added.rows * Screen_to_be_added.seats_per_row
            Screen_to_be_added.capacity=capacity
            
            rows_in_screen_hall=Screen_to_be_added.rows
            seat_per_row=Screen_to_be_added.seats_per_row
            All_seats:list[Seat]=[]
            seat_map_config:dict[str , Any]=Screen_to_be_added.seat_map_config
            if not seat_map_config:
                ...
            else:
                # for sec_is , sec_value in seat_map_config.items():
                seat_map_array:list=seat_map_config["sections"]
                for sec_is in seat_map_array:
                    type_is=sec_is["type"]
                    rows_labels_are:list[str]=sec_is["rows"]
                    for lable   in rows_labels_are:
                        for seat in range(1,rows_in_screen_hall+1):   
                           if seat < 10:
                               seat_name_is:str=f"{lable}0" + str(seat)
                               seat_in_screen_hall:Seat=Seat(row_label=lable , seat_number=seat_name_is , seat_type=type_is)
                               Screen_to_be_added.seats.append(seat_in_screen_hall)
                           else:
                               seat_name_is:str=f"{lable}" + str(seat)             #type:ignore 
                               seat_in_screen_hall:Seat=Seat(row_label=lable , seat_number=seat_name_is , seat_type=type_is) #type:ignore
                               Screen_to_be_added.seats.append(seat_in_screen_hall)                           
            
    
            theater_Is.screens.append(Screen_to_be_added)
            session.add(theater_Is)
            session.commit()
            session.refresh(Screen_to_be_added)
            return Screen_to_be_added
              
        except  HTTPException :
            raise;  
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Something unexpected happened while screen added to theater"
            )
    
    def screen_to_be_updated(self,screen_id:uuid.UUID ,screen_data:ScreenUpdate, session:Session):
        try:
                        
            screen_to_be_updated:Screen|None=session.get(Screen , screen_id)
            if not screen_to_be_updated:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Screen with id {screen_id} not found"
                )
            
            screen_data_dict=screen_data.model_dump(exclude_unset=True)
            
            if "rows" in screen_data_dict and "seats_per_row" in screen_data_dict:
                capacity:int=screen_data_dict["rows"] * screen_data_dict["seats_per_row"]
                screen_to_be_updated.capacity=capacity
            elif "rows" in screen_data_dict :
                capacity:int=screen_data_dict["rows"] * screen_to_be_updated.seats_per_row #type:ignore
                screen_to_be_updated.capacity=capacity
            elif "seats_per_row" in screen_data_dict:
                capacity:int=screen_to_be_updated.rows * screen_data_dict["seats_per_row"] #type:ignore
                screen_to_be_updated.capacity=capacity
            
            screen_to_be_updated.sqlmodel_update(screen_data_dict)
            
            session.add(screen_to_be_updated)
            session.commit()
            session.refresh(screen_to_be_updated)
            return screen_to_be_updated
              
        except  HTTPException :
            raise;  
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Something unexpected happened while screen updated to theater"
            ) from e 
    def screen_to_be_deleted(self,screen_id:uuid.UUID , session:Session):
        try:
            ...
            screen_is:Screen|None=session.get(Screen , screen_id)
            if not screen_is:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Screen with id {screen_id} not found"
                )
            
            screen_is.is_deleted=True
            screen_is.deleted_at=datetime.datetime.now(datetime.timezone.utc)
            session.add(screen_is)
            session.commit()
            return {"status":status.HTTP_202_ACCEPTED,"screen_id":screen_id,"message":"Screen Deleted Successfully"}    
            
            
        except HTTPException :
            raise;    
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Something unexpected happen while screen to be deleted with id  {screen_id}"
            )  from e 
    
    def add_seat(self , screen_id:uuid.UUID , seat_data:SeatCreate ,session:Session ):
        try:
            ...
            screen_is:Screen|None=session.get(Screen , screen_id)
            if not screen_is:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Screen with this id {screen_id }  Not Found!"
                )
            
            
            seat_to_be_added:Seat=Seat.model_validate(seat_data)
            screen_is.seats.append(seat_to_be_added)
            session.add(screen_is)
            session.commit()
            session.refresh(seat_to_be_added)
            return seat_to_be_added
                
        except HTTPException :
            raise    
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpedted error thrown while adding seat to screen with screen id  {screen_id}"
            )    from e
    
    def make_seat_deactive(self , screen_id :uuid.UUID  , seat_id:uuid.UUID , session:Session):
        try:
            
            screen_is:Screen|None=session.get(Screen , screen_id)
            if not screen_is:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Screen with this id {screen_id }  Not Found!"
                )
            seat_is:Seat|None=session.get(Seat , screen_id)
            if not seat_is:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Seat with this id {seat_id }  Not Found!"
                )
            
            seat_is.is_accessible=False
            session.add(seat_is)
            session.commit()
            session.refresh(seat_is)
            return seat_is
            
            # seats_in_screen_hall:list[Seat]=screen_is.seats
            # for     
                        
        except HTTPException :
            raise    
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpedted error thrown while adding seat to screen with screen id  {screen_id}"
            )    from e
    
    def make_seat_active(self , seat_id:uuid.UUID , session:Session):
        try:
            seat:Seat|None=session.get(Seat, seat_id)
            if not seat:
                 raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Seat with id {seat_id} is Not Found!"
                    )
            seat.is_accessible=True 
            session.add(seat)
            session.commit()
            return session.refresh(seat)    
                
        except HTTPException :
            raise    
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpedted error thrown while making  seat active   with seat id  {seat_id}"
            )    from e
                    
    
    def delete_seat(self , seat_id:uuid.UUID , session:Session):
        try:
            seat:Seat|None=session.get(Seat , seat_id)
            if not seat:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Seat with id {seat_id} is Not Found!"
                    )
            seat.deleted_at=datetime.datetime.now(datetime.timezone.utc)
            seat.is_deleted=True
            session.add(seat)
            session.commit()
            return {"seat_id":str(seat_id) ,"msg":"successfully deleted!" }
                
        except HTTPException :
            raise    
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpedted error thrown while deleting seat  with seat id  {seat_id}"
            )    from e
    
    
    
    
    def create_showtime(self  , showtime:ShowtimeCreate ,screen_id:uuid.UUID ,movie_id:uuid.UUID , session:Session):
        try:
            movie:Movie|None = session.get(Movie,movie_id)
            screen_hall:Screen|None = session.get(Screen,screen_id)
            
            if not movie:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"movie with id {movie_id}  Not Found"
                )
            if not screen_hall:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"screen hall  with id {screen_id}  Not Found"
                )
            showtime_is:Showtime=Showtime.model_validate(showtime)
            
            showtime_is.total_seats=screen_hall.capacity
            showtime_is.available_seats=screen_hall.capacity
            
            
            
            showtime_is.screen=screen_hall
            showtime_is.movie=movie
            
            
            session.add(showtime_is)
            session.commit()
            session.refresh(showtime_is)
            return showtime_is                            
                   
        except HTTPException :
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error  while creating showtime"
            )    
            
    def mark_showtime_to_cancelled(self, showtime_id:uuid.UUID,showtime_status:ShowtimeStatus,session:Session):
        try:
            showtime:Showtime|None=session.get(Showtime,showtime_id)
            if not showtime:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Showtime with id {showtime_id} not found"
                )
            
            showtime.status=showtime_status
            
            session.add(showtime_status)
            session.commit()
            return session.refresh(showtime)                
        except HTTPException :
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error  while creating showtime"
            )    
                    
    def update_Showtime(self, showtime_id:uuid.UUID ,showtime_update_data:ShowtimeUpdate, session:Session):
        try:
            
            showtime:Showtime|None=session.get(Showtime,showtime_id)
            if not showtime:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Showtime with id {showtime_id} not found"
                )
            showtime_update_data_dict:dict=   showtime_update_data.model_dump(exclude_unset=True)
            
            showtime.sqlmodel_update(showtime_update_data_dict)
            session.add(showtime)
            session.commit()
            return session.refresh(showtime) 
                    
        except HTTPException :
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error  while creating showtime"
            )    
    
    
    def get_theater_info(self  , user_data:UserInDb, session:Session):
        try:
            theater:Theater=user_data.haveThreator
            if not theater:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"theater not found"
                )
            
            threster_info:list[dict[str , Screen | list[Seat]]]=[]    
            
            for screen in theater.screens:
                threster_info.append(
                    {
                        screen.screen_type.value:screen,
                        "seats":screen.seats        
                    }
                )
            
            return threster_info    
        except Exception  as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error  while fetching theater info"
            ) from e 
     
    def get_screen_seats(self ,screen_id:uuid.UUID , session:Session ):
        try:
            screen:Screen|None=session.get(Screen,screen_id)
            if not screen:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"screen hall  with id {screen_id}  Not Found"
                )
            
            return screen.seats
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error  while fetching screen seats"
            )        
    
    def see_showtime_seats(self , showtime_id:uuid.UUID , session:Session):
        try:
            showtime:Showtime|None=session.get(Showtime,showtime_id)
            if not showtime:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Showtime with id {showtime_id} not found"
                )
            
            booked_seat_result:list[dict[str , Seat|str]]=[]
            
            bookings:list[Booking]=showtime.bookings
            for bookedseats in bookings:
                for singlebookedseat in bookedseats.booking_seats:
                   if singlebookedseat.status == BookingStatus.PENDING:
                       booked_seat_result.append({"seat":singlebookedseat.seat,"status":"pending"})
                   elif singlebookedseat.status == BookingStatus.CONFIRMED:
                       booked_seat_result.append({"seat":singlebookedseat.seat,"status":"confirmed"})
            
            return showtime.seats
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error  while fetching showtime seats"
            )        
    
    def get_all_showtimes_info(self, theater_id:uuid.UUID,session:Session,active:bool=False ):
        try:
            theater:Theater|None=session.get(Theater,theater_id)
            if not theater:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Theater with id {theater_id} not found"
                )
            
            all_showtimes:list[dict[str , Movie|Theater|Screen|Showtime]]=[]
            if active:      
                for screen in theater.screens:
                    for showtime in screen.showtimes:
                        if showtime.start_time > datetime.datetime.now(datetime.timezone.utc):
                            all_showtimes.append(showtime)
                    
                
                return all_showtimes 
            
            else :
                for screen in theater.screens:
                    all_showtimes.extend(screen.showtimes)
                return all_showtimes
            # all_showtimes.extend(screen.showtimes)
        except Exception  as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error  while fetching showtime info"
            ) from e 
    
    
    def get_all_booking_showtime(self , showtime_id:uuid.UUID , session:Session):
        try:
            showtime:Showtime|None=session.get(Showtime,showtime_id)
            if not showtime:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Showtime with id {showtime_id} not found"
                )
            
            booked_seat_result:list[dict[str , Seat|Screen|Showtime|UserInDb|Payment|str]]=[]
            
            bookings:list[Booking]=showtime.bookings
            for bookedseats in bookings:
                
                for singlebookedseat in bookedseats.booking_seats:
                   if singlebookedseat.status == BookingStatus.PENDING:
                       booked_seat_result.append({"showtime":showtime,"screen":showtime.screen,"user":bookedseats.user,"seat":singlebookedseat.seat,"status":"pending"})
                   elif singlebookedseat.status == BookingStatus.CONFIRMED:
                       booked_seat_result.append({"showtime":showtime,"screen":showtime.screen,"user":bookedseats.user,"seat":singlebookedseat.seat,"status":"confirmed"})
            
            return booked_seat_result
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error  while fetching showtime seats"
            )        

                
threator_cruds=TheraterCruds()            
        
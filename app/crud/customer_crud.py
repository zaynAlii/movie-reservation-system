from fastapi import HTTPException , Depends , status 
from typing import Annotated  ,Any
import  datetime
from sqlmodel import SQLModel , Session , select , and_
import uuid
from sqlmodel  import SQLModel , select , Session
from app.models.all_models  import (Showtime , ShowtimeCreate,UserInDb ,    #type:ignore 
                                    Seat , Booking  , Payment  , BookingStatus ,
                                    PaymentMethod,PaymentStatus,
                                    Movie , Theater , Screen , Seat , Review , 
                                    Booking_Seat , BookingCreate
                                    )     


import random 
import string

class CustomerCrud():
    
    def search_for_movies(self , moive_title:str , session:Session):
        try:
            movie:Movie=session.exec(select(Movie).where(Movie.title.ilike(f'%{moive_title}%'))).all()
            if not movie:
                return HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{moive_title} not found"
                )
            return movie

        except Exception  as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unknown error"
                ) from e  
                
    
    def get_movie_showtime(self , movie_name:str , session:Session):
        try:
            
            movies:list[Movie]=session.exec(select(Movie).where(Movie.title.ilike(f'%{movie_name}%'))).all() #type:ignore
            if not movies:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"showtime of this movie {movie_name} not found"
                )
            showtimes:list[tuple[Movie,list[dict[str , Showtime|Theater|Screen]]]]=[]
            for movie in movies:
                
                movie_showties=movie.showtimes
                active_showtimes:list[dict[str,Showtime|Theater]]=[]
                for showtime in movie_showties:
                    if showtime.start_time > datetime.datetime.now(datetime.timezone.utc):
                         active_showtimes.append({"showtime":showtime ,"screen":showtime.screen,"theater":showtime.screen.theater})
                showtimes.append((movie,active_showtimes))
            return showtimes    
                
        except Exception  as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unknown error"
                ) from e  
    def threater_screenhall_review(self  , showtime_id:uuid.UUID ,review_comment:str   , rating:int, session:Session):
        try:
            showtime:Showtime|None=session.get(Showtime , showtime_id)
            if not showtime:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"showtime with this id {showtime_id} ont found "
                )
            
            theater:Theater=showtime.screen.theater
            if not theater:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"theater with this showtime id {showtime_id} not found "
                )
            
            review:Review=Review(content=review_comment , rating=rating)
            review.theater=theater
            
            session.add(review)
            session.commit()
            return session.refresh(review)
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="unexpectd Error"
            )    
    
    def get_movie_reviews(self  , movie_id , session:Session):
        try:
            movie:Movie|None=session.get(Movie , movie_id)
            if not movie:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"movie with this id {movie_id} not found"
                )
            
            # reviews:list[Review]=session.exec(select(Review).where(Review.movie_id==movie_id)).all()
            reviews:list[Review]=movie.reviews
            if not reviews:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"reviews of this movie with this id {movie_id} not found"
                )
            
            return reviews
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                # detail=f"movie with this id {movie_id} not found"
                detail=f"Unexpected Thing happened"
            )     
    def get_threateer_reviews(self  , theater_id:uuid.UUID , session:Session):
        try:
            theater:Theater|None=session.get(Theater , theater_id)
            if not theater:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"theater with this id {theater_id} not found"
                )
            
            reviews:list[Review]=theater.havereview
            if not reviews:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"reviews of this theater with this id {theater_id} not found"
                )
            
            return reviews
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected Thing happened"
            )     
    def get_showtimes(self  , country:str  , state:str , city:str , session:Session):
        try:
            theaters:list[Theater]=session.exec(select(Theater).where(and_(Theater.country==country , Theater.state==state , Theater.city==city))).all() #type:ignore
            if not theaters:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"theater with this country {country} state {state} city {city} not found "
                )
            
            showtimes:list[tuple[Movie , list[dict[str  , Theater |Screen| Showtime]]]]=[]
            for theater in theaters:
                for screen in theater.screens: #3 
                   for showtime in screen.showtimes:
                       if showtime.start_time  > datetime.datetime.now(datetime.timezone.utc):
                            showtimes.append((showtime.movie , [{"showtime":showtime ,"screen":screen ,"theater":theater}]))
                            
            return showtimes
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="unexpectd Error"
            )   
    
    
    def movie_review(self  , movie_id:uuid.UUID , review_comment:str , rating:int , session:Session):
        try:
            movie:Movie|None=session.get(Movie , movie_id)
            if not movie:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"movie with this id {movie_id} not found"
                )
            
            review:Review=Review(content=review_comment , rating=rating)
            review.movie=movie
            
            session.add(review)
            session.commit()
            return session.refresh(review)
        
        except HTTPException:
            raise ;
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="unexpectd Error"
            )   
    
    # def show_seatmap_of_showtime_screen(self  , showtime_id:uuid.UUID , session:Session):
    #     try:
    #         showtime:Showtime|None=session.get(Showtime,showtime_id)
    #         if not showtime:
    #             return HTTPException(
    #                 status_code=status.HTTP_404_NOT_FOUND,
    #                 detail=f"Showtime with id {showtime_id} not found"
    #             )
    #         screen_seat_data:dict[str,Seat|Screen]={}
    #         if showtime.screen:    
    #            screen_seat_data["screen"]=showtime.screen
    #            screen_seat_data["seats"]=showtime.screen.seats
    #         return screen_seat_data
                
    #     except Exception  as e:
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail=f"Unknown error"
    #             ) from e  
            
    
    def booked_seats(self , user:UserInDb , session:Session):
        try:
            user_bookings=user.bookings
            user_booked_seats:list[dict[ str , str |Booking|Showtime|Screen|Movie |Seat |Theater]]=[]
            for user_booking in user_bookings:
                showtime=user_booking.showtime
                if showtime.start_time > datetime.datetime.now(datetime.timezone.utc):
                    for  singleseat in user_booking.booking_seats:
                        if singleseat.status =="pending":
                            user_booked_seats.append({"theater":showtime.screen.theater,"booking":user_booking ,"movie":showtime.movie,"showtime":showtime ,"screen":showtime.screen ,"seat":singleseat.seat,"status":singleseat.status.value})
                        elif singleseat.status == "confirmed":
                            user_booked_seats.append({"theater":showtime.screen.theater,"booking":user_booking ,"movie":showtime.movie,"showtime":showtime ,"screen":showtime.screen ,"seat":singleseat.seat,"status":singleseat.status.value})
                    # screen__hall_seats:list[Seat]=showtime.screen.seats
                    # for seat in screen__hall_seats:
                    #     if seat.user_id==user.id:
                    #         if seat.booked:
                    #             user_booked_seats.append({"theater":showtime.screen.theater ,"showtime":showtime ,"screen":showtime.screen ,"seat":seat})
        
            
            return user_booked_seats                        
                        
        except Exception as e:
            raise HTTPException (
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unknown error"
                ) from e  
            

    def create_booking(self , showtime_id:uuid.UUID ,data:BookingCreate, user_id:uuid.UUID,session:Session):
        try:
            showtime:Showtime|None=session.get(Showtime,showtime_id)
            if not showtime:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Showtime with id {showtime_id} not found"
                )
            
            if showtime.status=="soldout":
                return {"status":status.HTTP_400_BAD_REQUEST , "msg":"sold_out"}
            if showtime.available_seats <=0:
                showtime.status="sold_out"
                session.add(showtime)
                session.commit()
                return {"status":status.HTTP_400_BAD_REQUEST , "msg":"sold_out"}
                
            if showtime.available_seats < len(data.seat_data):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"You cant book {len(data.seat_data)} seats. Only  {showtime.available_seats}  are availble."
                )
                
            showtime.available_seats-=len(data.seat_data)
            showtime.held_seats+=len(data.seat_data)    
            # seat:Seat|None=session.get(Seat,seat_id)
            
            # if seat_ids :
            seat_ids_are=[]
            for seatdata in data.seat_data:
                seat_ids_are.append(seatdata["seat_id"])
                
            seats:list[Seat]=session.exec(select(Seat).where(Seat.id.in_(seat_ids_are))).all()  #type:ignore
            
            
            
            if not seats:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"seats not found"
                )
                
    
            user:UserInDb|None=session.get(UserInDb , user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"user with id {user_id} not found"
                )
          
            
            
            status_history:dict[str , Any]={
             "status":"pending",
             "at":datetime.datetime.now(datetime.timezone.utc).isoformat()    
            }
            
            date_is:str=datetime.datetime.now().strftime("%y%m%d")    
            random_5_chacaters:str=''.join(random.choices(string.ascii_uppercase + string.digits ,k=5))
            booking_is:Booking=Booking(
                status_history=[status_history] ,
                expires_at=data.expires_at,
                booking_number=f"BK-{date_is}-{random_5_chacaters}",
                )
            booking_is.showtime=showtime
            booking_is.user=user
            # booking_is.payment=payment_is
            for seat in seats:
                for seatdeta in data.seat_data:
                    if seat.id == seatdeta["seat_id"]:        
                        payment_is:Payment=Payment(
                            amount=seatdeta["amount"]
                        )
                booking_is.booking_seats.append(Booking_Seat(seat=seat , booked=True , payment=payment_is))
            session.add(booking_is)
            session.commit()
            
            return session.refresh(booking_is)
            
        except HTTPException :
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error  while creating showtime"
            ) from e 
    
    def  cancell_booking(self , booking_id:str  , seat_id:str, session:Session):
        try:
            seat_is:Seat|None=session.get(Seat ,seat_id )
            if not seat_is:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"seat with id{ booking_id}  is not found"
                )
            booking:Booking|None=session.get(Booking,booking_id)
            if not booking:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Booking with id{ booking_id}  is not found"
                )
            booking_seat:Booking_Seat=session.get(Booking_Seat , (booking_id , seat_id))
            if booking_seat.status == "cancelled":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Booking with id {booking_id} is already cancelled"
                    )
            showtime=booking.showtime
            if showtime.status == "completed":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Showtime is expired or completed . you cant cancel the ticket"
                ) 
                 
            if booking_seat.status == "pending":
                # user_seats:list[Seat]=user_is.seats
                booked_seats_are:list[Booking_Seat]=booking.booking_seats
                for booked_seat in booked_seats_are:
                    if booked_seat.seat_id == seat_id:
                        booked_seat.status=BookingStatus.CANCELLED
                        booking_seat.payment.status="cancelled"
                        break;
                    
                        
                
                # booking.status=BookingStatus.CANCELLED
                booking.cancelled_at=datetime.datetime.now(datetime.timezone.utc)
                booking.status_history.append({
                    "status":"cancalled",
                    "at":datetime.datetime.now(datetime.timezone.utc).isoformat()
                })
                # booking.payment.status="cancelled"       
                # booking.cancelled_at=datetime.datetime.now(datetime.timezone.utc)
                # seat_is.booked=False
                booking.showtime.available_seats+=1
                booking.showtime.held_seats-=1
                
                session.add_all([booking , booking_seat])
                session.commit()
                return session.refresh(booking)            
            if booking_seat.status == "confirmed":
                # if booking.showtime.status ==""
                booking_seat.status=BookingStatus.REFUNDED
                booking.cancelled_at=datetime.datetime.now(datetime.timezone.utc)
                booking.status_history.append({
                    "status":"cancalled",
                    "at":datetime.datetime.now(datetime.timezone.utc).isoformat()
                })
                booking_seat.payment.status="refunded"       
                booking_seat.payment.refunded_at=datetime.datetime.now(datetime.timezone.utc)
                booking_seat.payment.refund_amount=booking_seat.payment.amount-300 
                # seat_is.booked=False
                booking.showtime.available_seats +=1
                booking.showtime.held_seats-=1      
                # booking.cancelled_at=datetime.datetime.now(datetime.timezone.utc)
                session.add_all([booking , booking_seat])
                session.commit()
                return session.refresh(booking)            
                    
        except HTTPException :
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error  while creating showtime"
            ) from e 
            
    def confirm_booking(self , booking_id:uuid.UUID  , seat_id:uuid.UUID,data:PaymentMethod ,  session:Session):
        try:
            
            
            booking:Booking|None=session.get(Booking,booking_id)
            booked_seat:Booking_Seat|None=session.get(Booking_Seat , (booking_id , seat_id))
            if not booking:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Booking with id{ booking_id}  is not found"
                )
            if not booked_seat:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Booking not found!"
                )    
            
            if data.amount  < booked_seat.payment.amount:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"you are required to pay that much amount {booked_seat.payment.amount}. you are actually paying me that much {data.amount}"
                ) 
            
            booked_seat.status="confirmed"
            
            booking.confirmed_at=datetime.datetime.now(datetime.timezone.utc)
            
            booking.status_history.append({
                "status":"confirmed",
                "at":datetime.datetime.now(datetime.timezone.utc).isoformat()
            })
            
            
            booked_seat.payment.provider=data.provider
            booked_seat.payment.processed_at=datetime.datetime.now(datetime.timezone.utc)
            tran_id:str=''.join(random.choices(string.ascii_uppercase + string.digits ,k=9))

            booked_seat.payment.provider_transaction_id=tran_id
            booked_seat.payment.status="completed"            
            session.add_all([booking , booked_seat])
            session.commit()
            return session.refresh(booking)
 
        except HTTPException :
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error  while creating showtime"
            ) from e 
            

customer_crud=CustomerCrud()            
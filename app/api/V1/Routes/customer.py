from fastapi import APIRouter , HTTPException , status , Depends  ,Path
from app.crud.customer_crud  import customer_crud #type:ignore
from app.api.deps  import SESSION_Dependecy  , Get_currentUser , Current_active_user #type:ignore
from app.models.all_models import ReviewCreate , GetShowTimeByCountryCityState , BookingCreate  , PaymentMethod #type:ignore
from typing import Annotated
router=APIRouter()



@router.get("/search-by-movie/{movie_name}" , dependencies=[Depends(Get_currentUser)])
def search_by_movie(*,movie_name:str=Path() , session:SESSION_Dependecy):
    return customer_crud.search_for_movies(movie_name , session)


@router.get("/get-movies-active-showtimes/movie/{movie_name}" , dependencies=[Depends(Get_currentUser)])
def get_active_showtimes(*,movie_name:str=Path() , session:SESSION_Dependecy):
    return customer_crud.get_movie_showtime(movie_name , session)

@router.post("/give-review-rating-theater/showtime/{showtime_id}" , dependencies=[Depends(Get_currentUser)])
def give_review_rating(*,showtime_id:int=Path() ,review_data:ReviewCreate, session:SESSION_Dependecy):
    return customer_crud.threater_screenhall_review(showtime_id , review_data.content, review_data.rating, session)


@router.post("/give-review-rating-movie/movie/{movie_id}" , dependencies=[Depends(Get_currentUser)])
def give_review_rating_movie(*,movie_id:str=Path() ,review_data:ReviewCreate, session:SESSION_Dependecy):
    return customer_crud.movie_review(movie_id , review_data.content, review_data.rating, session)


@router.get("/get-movie-reviews/movie/{movie_id}" , dependencies=[Depends(Get_currentUser)])
def get_movie_reviews(*,movie_id:str=Path() , session:SESSION_Dependecy):
    return customer_crud.get_movie_reviews(movie_id , session)


@router.get("/get-theater-reviews/theater/{theater_id}" , dependencies=[Depends(Get_currentUser)])
def get_theater_reviews(*,theater_id:str=Path() , session:SESSION_Dependecy):
    return customer_crud.get_threateer_reviews(theater_id , session)



@router.get("/get-showtime-by-country-city-state",dependencies=[Depends(Get_currentUser)])
def get_showtime_by_country_city_state(*,place_details:GetShowTimeByCountryCityState , session:SESSION_Dependecy):
    return customer_crud.get_showtime_by_country_city_state(place_details.country ,place_details.city ,place_details.state , session)


@router.get("/get-booked-seats" , )
def get_booked_seats(*,user:Current_active_user , session:SESSION_Dependecy):
    return customer_crud.booked_seats(user , session)


@router.post("/book-seats/showtime/{showtime_id}")
def book_seats(*,showtime_id:Annotated[str , Path()] ,user:Current_active_user , booking_data:BookingCreate , session:SESSION_Dependecy):
    return customer_crud.create_booking( showtime_id , booking_data , user.id,  session)



@router.post("/cancel-boking/booking-id/{booking_id}/seat-id{seat_id}" , dependencies=[Depends(Get_currentUser)])
def cancel_booking(*,booking_id:Annotated[str , Path()] ,seat_id:Annotated[str , Path()]  , session:SESSION_Dependecy):
    return customer_crud.cancell_booking( booking_id , seat_id ,  session)


@router.post("/confirm-booking/booking-id/{booking_id}/seat-id{seat_id}" , dependencies=[Depends(Get_currentUser)])
def confirm_booking(*,booking_id:Annotated[str , Path()] ,seat_id:Annotated[str , Path()]   , payment_data:PaymentMethod, session:SESSION_Dependecy):
    return customer_crud.confirm_booking( booking_id , seat_id  , payment_data,  session)



# models/base.py
from datetime import datetime

from uuid import UUID, uuid4
import enum
from decimal import Decimal
from enum import Enum as PyEnum
from typing import TYPE_CHECKING

from datetime import date, timedelta

from sqlalchemy import Column, DateTime,Text,Date , ARRAY ,func, Index, text ,Numeric, String , Integer , Enum as SQLEnum , Boolean , Float , ForeignKey , Index , CheckConstraint , UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB

from sqlalchemy.orm import declared_attr
from typing import List, Optional, Dict, Any, TYPE_CHECKING
# if TYPE_CHECKING:
#     from typing import Mapped
# else:
#     from sqlalchemy.orm import Mapped



from sqlmodel import SQLModel, Field, Relationship

# from movie_reservation_system.app.models.UserModel import UserRefreshToken


if TYPE_CHECKING:
    from .refresh_model import UserRefreshToken


class TimestampMixin:
    """Professional-grade timestamp handling with timezone awareness"""
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))


class SoftDeleteMixin:
    """Soft delete pattern for GDPR compliance and audit trails"""
    deleted_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    is_deleted: bool = Field(default=False, sa_column=Column(Boolean, default=False, index=True))

    @property
    def is_active(self) -> bool:
        return not self.is_deleted


class AuditMixin(SQLModel):
    """Track who created/modified records"""
    created_by: Optional[UUID] = Field(default=None, foreign_key="users.id")
    updated_by: Optional[UUID] = Field(default=None, foreign_key="users.id")
    
    
    



class UserRole(str, PyEnum):
    CUSTOMER = "customer"
    THEATER_MANAGER = "theater_manager"
    ADMIN = "admin"
    # SUPPORT = "support"




class User(SQLModel):
    
    email: str = Field(sa_column=Column(String(255), unique=True, index=True, nullable=False))
    
    username:str=Field(sa_column=Column(String(100), unique=True, index=True, nullable=False))
    
    # Profile
    first_name: str = Field(sa_column=Column(String(100), nullable=False))
    last_name: str = Field(sa_column=Column(String(100), nullable=False))
    phone: Optional[str] = Field(default=None, sa_column=Column(String(20), unique=True, index=True))
    
    
    role: UserRole = Field(default=UserRole.CUSTOMER, sa_column=Column(SQLEnum(UserRole) , nullable=False))
    is_verified: bool = Field(default=False)
    
        # Professional pattern: composite indexes for common queries

class UserPublic(User):
    id: UUID
    
class UserIn(User):
    password:str=Field(min_length=10 , max_length=25)    

class  UserInDb(User,table=True):

    __tablename__ = "users"
    # __allow_unmapped__ = True

    id: UUID = Field(default_factory=uuid4, sa_column=Column(PG_UUID(as_uuid=True), primary_key=True))
    hashed_password: str = Field(sa_column=Column(String(255), nullable=False))
    created_at: datetime | None = Field(default=None,sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime |None= Field(default=None,sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))
    deleted_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    is_deleted: bool = Field(default=False, sa_column=Column(Boolean, default=False, index=True))
    bookings: List["Booking"] = Relationship(back_populates="user")
    reviews: List["Review"] = Relationship(back_populates="user")
    haveRefreshToken:'UserRefreshToken'=Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "cascade":"all , delete-orphan"
        })
    haveThreator:'Theater'=Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "cascade":"all , delete-orphan"
        }
    )
    # seats:list['Seat']=Relationship(back_populates="user")
    __table_args__=(
        Index('idx_user_active_role', 'role','is_deleted'),
        Index('idx_user_email_verified', 'email', 'is_verified'),
    )


# Threater Mnagent
        # models/theaters.py


class SeatType(str, PyEnum):
    STANDARD = "standard"
    PREMIUM = "premium"
    VIP = "vip"
    ACCESSIBLE = "accessible"  # ADA compliance


class ScreenType(str, PyEnum):
    STANDARD = "standard"
    IMAX = "imax"
    DOLBY_CINEMA = "dolby_cinema"
    _3D = "3d"
    _4DX = "4dx"


class ThreaterCreate(SQLModel):
    ...
    name: str = Field(min_length=7, max_length=499)
    address: str =Field(min_length=3, max_length=499)
    city: str = Field(min_length=3, max_length=100)
    state: str = Field(min_length=3, max_length=100)
    country: str = Field(min_length=3, max_length=100)
    zip_code: str = Field(min_length=3, max_length=20)
    phone: str = Field(min_length=3, max_length=20)
    email: Optional[str] = Field(default=None, max_length=100)

class ThreatorOut(ThreaterCreate):
    id:UUID
    created_at: datetime

class ThreaterUpdate(SQLModel):
    name: str |None = Field(default=None , min_length=7, max_length=499)
    address: str | None =Field(default=None,min_length=3, max_length=499)
    city: str | None= Field(default=None,min_length=3, max_length=100)
    state: str | None  = Field(default=None,min_length=3, max_length=100)
    country: str |None= Field(default=None,min_length=3, max_length=100)
    zip_code: str |None= Field(default=None,min_length=3, max_length=20)
    phone: str|None = Field(default=None,min_length=3, max_length=20)
    email: Optional[str] = Field(default=None, max_length=100)
    
        

class Theater(SQLModel,table=True):
    __tablename__ = "theaters"
    # __allow_unmapped__ = True

    id: UUID = Field(default_factory=uuid4, sa_column=Column(PG_UUID(as_uuid=True), primary_key=True))
    name: str = Field(sa_column=Column(String(200), nullable=False))
    
    user_id:UUID|None=Field(default=None,foreign_key="users.id")
    
    # Location (normalized for analytics)
    address: str = Field(sa_column=Column(String(500), nullable=False))
    city: str = Field(sa_column=Column(String(100), nullable=False, index=True))
    state: str = Field(sa_column=Column(String(100), nullable=False))
    country: str = Field(sa_column=Column(String(100), nullable=False))
    zip_code: str = Field(sa_column=Column(String(20), nullable=False))

    # Contact
    phone: str = Field(sa_column=Column(String(20), nullable=False))
    email: Optional[str] = Field(default=None, sa_column=Column(String(255)))

    # Metadata
    amenities: Dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(JSONB, default=dict)  # {parking: true, food_court: true}
    )
    total_screens: int = Field(default=0, sa_column=Column(Integer, default=0))

    # Timestamp fields
    created_at: datetime |None= Field(default=None,sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime |None = Field(default=None,sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))
    deleted_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    is_deleted: bool = Field(default=False, sa_column=Column(Boolean, default=False, index=True))

    # Relationships
    screens: List["Screen"] = Relationship(back_populates="theater")
    user:'UserInDb'=Relationship(
        back_populates="haveThreator"
    )
    havereview:list['Review']=Relationship(back_populates="theater")
    # Professional: GIN index for JSONB queries
    __table_args__ = (

            Index('idx_theater_location','state' ,'city' ),
            # Index('idx_theater_coords', 'latitude', 'longitude'),
            Index('idx_theater_amenities', 'amenities', postgresql_using='gin'),

        )


class ScreenCreate(SQLModel):
     
    
    name: str = Field(max_length=100)  # "Screen 1", "IMAX Hall"

    # Technical specs
    screen_type: ScreenType = Field(default=ScreenType.STANDARD)
    # capacity: int

    # Seat map configuration (normalized but flexible)
    rows: int 
    seats_per_row: int 
    seat_map_config: Dict[str, Any] = Field( description= "Layout configuration: {layout: 'standard', row_labels: ['A', 'B'], gaps: [4, 12]}")

class ScreenUpdate(SQLModel):
    name: str |None= Field(default=None,max_length=100)  # "Screen 1", "IMAX Hall"

    # Technical specs
    screen_type: ScreenType = Field(default=ScreenType.STANDARD)
    # capacity: int |None=None

    # Seat map configuration (normalized but flexible)
    rows: int |None=None
    seats_per_row: int |None=None
    seat_map_config: Dict[str, Any]|None = Field(
        default=None
        # {layout: "standard", row_labels: ["A", "B"], gaps: [4, 12]}
    )
        
class ScreenOut(ScreenCreate):
    id:UUID
    created_at: datetime   
    capacity:int         


class Screen(SQLModel,table=True):
    __tablename__ = "screens"

    id: UUID = Field(default_factory=uuid4, sa_column=Column(PG_UUID(as_uuid=True), primary_key=True))
    theater_id: UUID |None= Field(default=None,foreign_key="theaters.id", index=True)
    name: str = Field(sa_column=Column(String(100), nullable=False))  # "Screen 1", "IMAX Hall"

    # Technical specs
    screen_type: ScreenType = Field(default=ScreenType.STANDARD)
    capacity: int |None= Field(default=None,sa_column=Column(Integer, nullable=False))

    # Seat map configuration (normalized but flexible)
    rows: int = Field(sa_column=Column(Integer, nullable=False))
    seats_per_row: int = Field(sa_column=Column(Integer, nullable=False))
    seat_map_config: Dict[str, Any] = Field(
        sa_column=Column(JSONB, nullable=False)
                    #         {
                    #   "sections": [
                    #     {
                    #       "type": "Standard",
                    #       "rows": ["A", "B", "C", "D"],
                    #       "seats_per_row": 40,
                    #       "gaps": [4, 12],
                    
                    #     },
                    #     {
                    #       "type": "VIP",
                    #       "rows": ["E", "F", "G", "H"],
                    #       "seats_per_row": 20,
                    #       "gaps": [5, 15],
                    #
                    #     },
                    #     {
                    #       "type": "Premium",
                    #       "rows": ["I", "J"],
                    #       "seats_per_row": 15,
                    #       "gaps": [7],
                    \
                    #     }
                    #   ]
                    # }
    )

    # Timestamp fields
    created_at: datetime|None = Field(default=None,sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime|None = Field(default=None,sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))
    deleted_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    is_deleted: bool = Field(default=False, sa_column=Column(Boolean, default=False, index=True))

    # Relationships
    theater: Theater = Relationship(back_populates="screens")
    seats: List["Seat"] = Relationship(back_populates="screen")
    showtimes: List["Showtime"] = Relationship(back_populates="screen")


    __table_args__= (

            UniqueConstraint('theater_id', 'name', name='uq_screen_theater_name'),
            CheckConstraint('capacity > 0', name='chk_screen_capacity_positive'),

       )
    
class SeatCreate(SQLModel):
    row_label: str 
    seat_number: int 
    seat_type: SeatType = Field(default=SeatType.STANDARD )


class SeatOut(SeatCreate):
    id:UUID
    created_at:datetime

class Seat(SQLModel,table=True):
    __tablename__ = "seats"

    id: UUID = Field(default_factory=uuid4, sa_column=Column(PG_UUID(as_uuid=True), primary_key=True))
    screen_id: UUID |None = Field(default=None,foreign_key="screens.id", index=True)
    # user_id:UUID|None=Field(default=None,foreign_key="users.id")
    # booking_id:UUID|None=Field(default=None,foreign_key="bookings.id")
    
    # user_id:UUID|None=Field(default=None,foreign_key="users.id", index=True)
    # Human-readable identifier: "A12", "B5"
    row_label: str = Field(sa_column=Column(String(5), nullable=False))
    seat_number: int = Field(sa_column=Column(Integer, nullable=False))

    # Tiered pricing support
    seat_type: SeatType = Field(default=SeatType.STANDARD , sa_column=Column(SQLEnum(SeatType), nullable=False))
    
    # booked:bool|None=Field(default=False)

    is_accessible: bool|None = Field(default=True)

    # Timestamp fields
    created_at: datetime |None = Field(default=None,sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime |None= Field(default=None,sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))
    deleted_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    is_deleted: bool = Field(default=False, sa_column=Column(Boolean, default=False, index=True))

    # Relationships
    screen: Screen = Relationship(back_populates="seats")
    user:UserInDb=Relationship(back_populates="seats")
    booking_seat:list['Booking_Seat']=Relationship(back_populates="seat")
    # booking:'Booking'=Relationship(back_populates="seat")
    __table_args__= (

            UniqueConstraint('screen_id', 'row_label', 'seat_number', name='uq_seat_location'),
            Index('idx_seat_screen_type', 'seat_type','screen_id'),

    )
        




class Rating(str, PyEnum):
    G = "G"
    PG = "PG"
    PG_13 = "PG-13"
    R = "R"
    NC_17 = "NC-17"


class MovieStatus(str, PyEnum):
    UPCOMING = "upcoming"
    NOW_SHOWING = "now_showing"
    ENDED = "ended"


# class Genera(SQLModel , table=True):
#     __tablename__ = "genera"
    
#     id: UUID = Field(default_factory=uuid4, sa_column=Column(PG_UUID(as_uuid=True), primary_key=True))
#     name: str = Field(sa_column=Column(String(100), unique=True, index=True, nullable=False))
    # description: Optional[str] = Field(default=None, sa_column=Column(Text))


class MovieIn(SQLModel):
    ...
    title: str 
    description: str  

    # Classification
    genres: List[str]
    rating: Rating 
    duration_minutes: int 

    # Media

    # Dates
    release_date: date 
    end_date: Optional[date] = Field(default=None)  # When it stops showing

    # Metadata
    language: str = Field(default="en")
    director: Optional[str] = Field(default=None)
    cast: List[str] = Field(default_factory=list)
    movie_metadata: Dict[str, Any] = Field(default_factory=dict)

    # Status (derived from dates, but cached for performance)
    status: MovieStatus = Field(default=MovieStatus.UPCOMING)

class MovieOut(MovieIn):
    id:UUID
    created_at: datetime 
    updated_at: datetime 
    poster_url: Optional[str] = Field(default=None )
    backdrop_url: Optional[str] = Field(default=None)
    trailer_url: Optional[str] = Field(default=None)

class MovieUpdate(SQLModel):
    title: str |None=None
    description: str |None=None

    # Classification
    genres: List[str]|None = None
    rating: Rating |None=  None 
    duration_minutes: int |None=None 

    # Media

    # Dates
    release_date: date |None = None
    end_date: date |None = None  # When it stops showing

    # Metadata
    language: str |  None = None  
    director: Optional[str] = Field(default=None)
    cast: List[str] | None =None
    # movie_metadata: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB ))

    # Status (derived from dates, but cached for performance)
    status: MovieStatus |None= Field(default=MovieStatus.UPCOMING)

    

class Movie(SQLModel,table=True):
    __tablename__ = "movies"

    id: UUID = Field(default_factory=uuid4, sa_column=Column(PG_UUID(as_uuid=True), primary_key=True))
    title: str = Field(sa_column=Column(String(300), nullable=False, index=True))
    description: str = Field(sa_column=Column(Text, nullable=False))

    # Classification
    genres: List[str] = Field(sa_column=Column(ARRAY(String(50))))
    rating: Rating = Field( sa_column=Column(SQLEnum(Rating), nullable=False))
    duration_minutes: int = Field(sa_column=Column(Integer, nullable=False))

    # Media

    # Dates
    release_date: date = Field(sa_column=Column(Date, nullable=False, index=True))
    end_date: Optional[date] = Field(default=None)  # When it stops showing

    # Metadata
    language: str = Field(default="en", sa_column=Column(String(10)))
    director: Optional[str] = Field(default=None, sa_column=Column(String(200)))
    cast: List[str] = Field(default_factory=list,sa_column=Column(ARRAY(String(200)), default=list))
    movie_metadata: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB ))

    # Status (derived from dates, but cached for performance)
    status: MovieStatus = Field(default=MovieStatus.UPCOMING)
    poster_url: Optional[str] = Field(default=None, sa_column=Column(String(500)))
    backdrop_url: Optional[str] = Field(default=None, sa_column=Column(String(500)))
    trailer_url: Optional[str] = Field(default=None, sa_column=Column(String(500)))


    # Basic info

    # Analytics
    average_rating: float = Field(default=0.0, sa_column=Column(Float))
    total_reviews: int = Field(default=0)

    # Timestamp fields
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))
    deleted_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    is_deleted: bool = Field(default=False, sa_column=Column(Boolean, index=True))

    # Relationships
    showtimes: List["Showtime"] = Relationship(back_populates="movie")
    reviews: List["Review"] = Relationship(back_populates="movie")

    __table_args__ = (
            # Full-text search index (PostgreSQL tsvector)
            # Index(
            #     'idx_movie_fts',
            #     text("to_tsvector('english', title || ' ' || coalesce(description, ''))"),
            #     postgresql_using='gin'
            # ),
            Index('idx_movie_status_dates', 'status', 'release_date'),
            Index('idx_movie_genres', 'genres', postgresql_using='gin'),
        )
        






class ShowtimeStatus(str, PyEnum):
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    SOLD_OUT = "sold_out"


class  ShowtimeCreate(SQLModel):
    ...
    start_time: datetime 
    end_time: datetime 
    base_price: Decimal = Field(
        sa_column=Column(Numeric(10, 2), nullable=False)  # 99999999.99 max
    )
    price_multiplier: dict[str, Any] 

class  ShowtimeUpdate(SQLModel):
    ...
    start_time: datetime | None=None 
    end_time: datetime | None=None
    base_price: Decimal| None = Field(
        default=None  # 99999999.99 max
    )
    price_multiplier: dict[str, Any]| None=None 

    
    
class ShowTimeOut(ShowtimeCreate):
    id:UUID
    created_at:datetime  
    total_seats: int
    available_seats: int
    held_seats:int
    
class GetShowTimeByCountryCityState(SQLModel):
    country:str
    city:str
    state:str

class Showtime(SQLModel,table=True):
    __tablename__ = "showtimes"

    id: UUID = Field(default_factory=uuid4, sa_column=Column(PG_UUID(as_uuid=True), primary_key=True))
    movie_id: UUID|None = Field(default=None , foreign_key="movies.id", index=True)
    screen_id: UUID|None = Field(default=None ,foreign_key="screens.id", index=True)

    # Timing (timezone-aware)
    start_time: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False, index=True))
    end_time: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))

    # Dynamic pricing configuration
    base_price: Decimal = Field(
        sa_column=Column(Numeric(10, 2), nullable=False)  # 99999999.99 max
    )
    price_multiplier: Dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(JSONB)
        # {vip: 1.5, premium: 1.2, weekend: 1.3}
    )
    rating:int|None=Field(default=None,sa_column=Column(Integer , nullable=True))
    # Inventory management
    total_seats: int|None = Field(default=None,nullable=False)
    available_seats: int|None = Field(default=None,nullable=False)
    held_seats: int |None= Field(default=0)  # Seats in "pending" bookings

    # Status
    status: ShowtimeStatus = Field(default=ShowtimeStatus.SCHEDULED)
    # is_active: bool = Field(default=True)

    # Timestamp fields
    created_at: datetime |None = Field(default=None,sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime |None= Field(default=None,sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))
    deleted_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    is_deleted: bool = Field(default=False, sa_column=Column(Boolean, default=False, index=True))

    # Relationships
    movie: "Movie" = Relationship(back_populates="showtimes")
    screen: "Screen" = Relationship(back_populates="showtimes")
    bookings: List["Booking"] = Relationship(back_populates="showtime")
    # seat_locks: List["SeatLock"] = Relationship(back_populates="showtime")

    __table_args__ = (
            UniqueConstraint('screen_id', 'start_time', name='uq_showtime_screen_time'),
            CheckConstraint('end_time > start_time', name='chk_showtime_duration'),
            CheckConstraint('available_seats >= 0', name='chk_available_seats_non_negative'),
            CheckConstraint('available_seats + held_seats <= total_seats', name='chk_seat_inventory'),
            Index('idx_showtime_active_start', 'is_deleted', 'start_time'),
    )
        

# class SeatBookingDATA(SQLModel):
    # seat;

class BookingStatus(str, PyEnum):
    PENDING = "pending"           # Just created, payment not started
    PAYMENT_PENDING = "payment_pending"  # User in payment flow
    CONFIRMED = "confirmed"       # Paid successfully
    CANCELLED = "cancelled"       # User cancelled or payment failed
    REFUNDED = "refunded"         # Money returned
    COMPLETED = "completed"       # Show attended


class PaymentStatus(str, PyEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"       # User cancelled or payment failed
    

class BookingCreate(SQLModel):
        
    seat_data:list[dict[str , str|int]]
        #[{
        #  "seat_id":*******  
        #  "price":*******
        # },
        # {
        #   "seat_id":*******  
        #  "price":*******
        # }]
    expires_at:datetime    


class BookingCreateTimingStatus(SQLModel):
    expires_at: datetime |None=None
    confirmed_at: Optional[datetime] = Field(default=None)
    cancelled_at: Optional[datetime] = Field(default=None)

class Booking(SQLModel,table=True):
    __tablename__ = "bookings"

    id: UUID = Field(default_factory=uuid4, sa_column=Column(PG_UUID(as_uuid=True), primary_key=True))

    # References
    user_id: UUID = Field(foreign_key="users.id", index=True)
    showtime_id: UUID = Field(foreign_key="showtimes.id", index=True)

    # Booking identification (human-readable)
    booking_number: str = Field(
          sa_column=Column(String(20), unique=True, index=True, nullable=False)
        # Format: BK-20240201-XXXXX
    )


    # Status workflow
    # status: BookingStatus = Field(default=BookingStatus.PENDING , sa_column=Column(SQLEnum(BookingStatus), nullable=False))
    status_history: List[Dict[str, Any]] = Field(
        default_factory=list,
        sa_column=Column(JSONB)
        # [{status: "pending", at: "2024-02-01T10:00:00", by: "system"}]
    )
    
    
    # booked_seats:int = Field(default=0,sa_column=Column(Integer , nullable=False))
    
    # Timing
    expires_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    confirmed_at: Optional[datetime] = Field(default=None)
    cancelled_at: Optional[datetime] = Field(default=None)

    # Timestamp fields
    created_at: datetime |None= Field(default=None,sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime |None = Field(default=None,sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))
    deleted_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    is_deleted: bool = Field(default=False, sa_column=Column(Boolean, default=False, index=True))



    # Relationships
    user: "UserInDb" = Relationship(back_populates="bookings")
    showtime: "Showtime" = Relationship(back_populates="bookings")
    # seat:Seat=Relationship(back_populates="booking")
    # items: List["BookingItem"] = Relationship(back_populates="booking")
    booking_seats: List["Booking_Seat"] = Relationship(back_populates="booking")
    # payment: Optional["Payment"] = Relationship(back_populates="booking")
    # review: Optional["Review"] = Relationship(back_populates="booking")
    __table_args__ = (
            Index('idx_booking_user_status', 'user_id',),
            # Index('idx_booking_user_status', 'user_id', 'status'),
            Index('idx_booking_showtime_status', 'showtime_id'),
            # Index('idx_booking_showtime_status', 'showtime_id', 'status'),
            Index('idx_booking_created', 'created_at'),  # For reporting
            # CheckConstraint('total_amount >= 0', name='chk_booking_amount_positive'),
    )



# 1  :  1000  standard
# 2:  2000     premium
# 3:  3000    vip  




class Booking_Seat(SQLModel,table=True):

    # id:UUID=Field(default_factory=uuid4 , sa_column=Column(PG_UUID(as_uuid=True), primary_key=True))
    seat_id: UUID |None= Field(default=None,foreign_key="seats.id", index=True , primary_key=True)
    booking_id: UUID |None= Field(default=None,foreign_key="bookings.id", index=True , primary_key=True)
    payment_id:UUID|None= Field(default=None,foreign_key="payments.id", index=True)
    booked:bool=Field(default=False)
    status:BookingStatus=Field(default=BookingStatus.PENDING, sa_column=Column(SQLEnum(BookingStatus, name='bookingstatus', create_type=False), nullable=False))
    
    payment:'Payment'=Relationship(back_populates="booking_seat_payment")
    booking:Booking=Relationship(back_populates="booking_seats")
    seat:Seat=Relationship(back_populates="booking_seats")
    
    
        
# 
class PaymentMethod(SQLModel):
    provider:str ="easypaisa"
    amount:str=Field(gt=0)
    mobile_number:str
class Payment(SQLModel,table=True):
    __tablename__ = "payments"

    id: UUID = Field(default_factory=uuid4, sa_column=Column(PG_UUID(as_uuid=True), primary_key=True))
    # booking_id: UUID = Field(foreign_key="bookings.id", unique=True, index=True)

    # Transaction details
    provider: str = Field(sa_column=Column(String(50), nullable=True))  # stripe, paypal, etc.
    provider_transaction_id: str = Field(sa_column=Column(String(200), nullable=True, index=True))
    amount: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=True))
    currency: str = Field(default="PKR", sa_column=Column(String(3)))
    
    # Status
    status: PaymentStatus = Field(default=PaymentStatus.PENDING)
    error_message: Optional[str] = Field(default=None, sa_column=Column(String(500)))

    # Timestamps
    processed_at: Optional[datetime] = Field(default=None)
    refunded_at: Optional[datetime] = Field(default=None)
    refund_amount: Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(10, 2)))

    # Timestamp fields
    created_at: datetime|None = Field(default=None,sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime |None= Field(default=None,sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))
    deleted_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    is_deleted: bool = Field(default=False, sa_column=Column(Boolean, default=False, index=True))

    # Raw response for debugging/disputes
    provider_metadata: Dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(JSONB)
    )

    # Relationships
    # booking: Booking = Relationship(back_populates="payment")
    booking_seat_payment:Booking_Seat=Relationship(back_populates="payment")
    __table_args__ = (
            Index('idx_payment_provider_txn', 'provider', 'provider_transaction_id'),
            Index('idx_payment_status_date', 'status', 'processed_at'),
    )
        
#reviews  
# models/reviews.py


class ReviewCreate(SQLModel):
    rating: int    # 1-10 scale (more granular than 5-star)
    content: str 

class Review(SQLModel,table=True):
    __tablename__ = "reviews"

    id: UUID = Field(default_factory=uuid4, sa_column=Column(PG_UUID(as_uuid=True), primary_key=True))
    user_id: UUID = Field(foreign_key="users.id", index=True)
    movie_id: UUID |None= Field(default=None,foreign_key="movies.id", index=True)
    theater_id: UUID |None= Field(default=None,foreign_key="theaters.id", unique=True)  # One review per booking

    # Content
    rating: int = Field(sa_column=Column(Integer, nullable=False))  # 1-10 scale (more granular than 5-star)
    # title: Optional[str] = Field(default=None, sa_column=Column(String(200)))
    content: str = Field(sa_column=Column(Text, nullable=False))

    # Moderation
    # is_approved: bool = Field(default=False)
    # moderated_at: Optional[datetime] = Field(default=None)
    # moderation_notes: Optional[str] = Field(default=None, sa_column=Column(String(500)))

    # Helpfulness
    helpful_count: int = Field(default=0)
    not_helpful_count: int = Field(default=0)

    # Timestamp fields
    created_at: datetime|None = Field(default=None,sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime|None = Field(default=None,sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))
    deleted_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    is_deleted: bool = Field(default=False, sa_column=Column(Boolean, default=False, index=True))

    # Relationships
    user: "UserInDb" = Relationship(back_populates="reviews")
    movie: "Movie" = Relationship(back_populates="reviews")
    theater:Theater=Relationship(back_populates="havereview")
    # booking: "Booking" = Relationship(back_populates="review")  # Verify they actually watched it

    __table_args__ = (
            CheckConstraint('rating >= 1 AND rating <= 10', name='chk_review_rating_range'),
            # Index('idx_review_movie_approved', 'movie_id', 'is_approved', 'created_at'),
            Index('idx_review_movie_approved', 'movie_id',  'created_at'),
            Index('idx_review_user_movie', 'user_id', 'movie_id'),
            )

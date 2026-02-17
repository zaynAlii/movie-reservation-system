# Movie Reservation System

A modern, scalable movie theater reservation system built with FastAPI, SQLAlchemy, PostgreSQL, and Docker.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0+-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-orange)
![PostgreSQL](blue) ![Docker](https://img.shields.io/badge/Docker-Ready-blue)

## 🚀 Features

### User Management
- **Role-based Access Control**: Support for three user roles:
  - `Customer`: Book movie tickets
  - `Theater Manager`: Manage theaters, screens, showtimes
  - `Admin`: Full system access
- **Authentication**: JWT-based authentication with access and refresh tokens
- **Password Security**: Secure password hashing with bcrypt/argon2

### Movie Management
- Browse movies with detailed information
- Movie ratings and genres
- Release and end dates tracking
- Movie metadata storage (poster, backdrop, trailer URLs)

### Theater Management
- Multi-theater support
- Screen management with different screen types (Standard, IMAX, Dolby Cinema, 3D, 4DX)
- Seat configuration with row labels and seat numbers
- Seat types (Standard, Premium, VIP, Accessible)

### Booking System

- Booking status workflow:
  - `PENDING`: Just created, payment not started

  - `CONFIRMED`: Payment successful
  - `CANCELLED`: User cancelled or payment failed
  - `REFUNDED`: Money returned
  - `COMPLETED`: Show attended
- Booking history tracking
- Seat selection for bookings

### Showtime Management
- Schedule showtimes for movies
- Dynamic pricing configuration

- Available, held, and total seats management


### Reviews & Ratings
- Movie reviews with ratings (1-10 scale)
- Theater reviews
- Helpfulness voting system

## 🏗️ Architecture

```
movie_reservation_system/
├── app/
│   ├── api/              # API routes
│   │   └── V1/
│   │       └── Routes/   # Endpoint handlers
│   ├── core/             # Core configurations
│   │   ├── db_settings.py
│   │   ├── security.py
│   │   └── settings.py
│   ├── crud/            # Database operations
│   ├── models/           # SQLModel definitions
│   └── shemas/          # Pydantic schemas
├── migrations/           # Alembic migrations
├── main.py              # Application entry point
└── alembic.ini          # Alembic configuration
```

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLModel (SQLAlchemy)
- **Database**: PostgreSQL
- **Authentication**: JWT (PyJWT)
- **Password Hashing**: Bcrypt/Argon2
- **Migrations**: Alembic
- **Containerization**: Docker
- **Validation**: Pydantic

## 🚦 Getting Started

### Prerequisites

- Python 3.13+
- PostgreSQL
- Docker & Docker Compose (optional)

### Installation

1. **Clone the repository**
   
```
bash
   cd movie_reservation_system
   
```

2. **Create and activate virtual environment**
   

4. **Configure environment variables**
   
   Edit `.env` file:
   
```
env
   DataBase_Url="postgresql://username:password@host:5432/database_name"
   secret_key="your-secret-key"
   Algorithm=HS256
   Expire_ACCESS_TOKEN=3   # minutes
   Expire_Refresh_TOKEN=7  # days
   
```

5. **Run database migrations**
   
```
bash
   alembic upgrade head
   
```

6. **Start the development server**
   
```
bash
   uv run fastapi dev main.py
   # Or
   uvicorn main:app --reload
   
```

7. **Access the API documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Using Docker

1. **Build and run with Docker**
   
```
bash
   docker build -t movie-reservation-system .
   docker run -p 8000:8000 movie-reservation-system
   
```

2. **Using Docker Compose**
   
```
bash
   docker-compose up --build
   
```

## 📡 API Endpoints

### Authentication
- `POST /api/V1/auth/register` - Register new user
- `POST /api/V1/auth/login` - Login user
- `POST /api/V1/auth/refresh` - Refresh access token
- `POST /api/V1/auth/logout` - Logout user

### Users
- `GET /api/V1/users/` - Get all users
- `GET /api/V1/users/{user_id}` - Get user by ID
- `PUT /api/V1/users/{user_id}` - Update user
- `DELETE /api/V1/users/{user_id}` - Delete user

### Theaters
- `POST /api/V1/theaters/` - Create theater
- `GET /api/V1/theaters/` - Get all theaters
- `GET /api/V1/theaters/{theater_id}` - Get theater details
- `PUT /api/V1/theaters/{theater_id}` - Update theater
- `DELETE /api/V1/theaters/{theater_id}` - Delete theater

### Movies
- `POST /api/V1/movies/` - Create movie
- `GET /api/V1/movies/` - Get all movies
- `GET /api/V1/movies/{movie_id}` - Get movie details
- `PUT /api/V1/movies/{movie_id}` - Update movie
- `DELETE /api/V1/movies/{movie_id}` - Delete movie

### Showtimes
- `POST /api/V1/showtimes/` - Create showtime
- `GET /api/V1/showtimes/` - Get all showtimes
- `GET /api/V1/showtimes/{showtime_id}` - Get showtime details
- `PUT /api/V1/showtimes/{showtime_id}` - Update showtime
- `DELETE /api/V1/showtimes/{showtime_id}` - Delete showtime

### Bookings
- `POST /api/V1/bookings/` - Create booking
- `GET /api/V1/bookings/` - Get all bookings
- `GET /api/V1/bookings/{booking_id}` - Get booking details
- `PUT /api/V1/bookings/{booking_id}` - Update booking
- `DELETE /api/V1/bookings/{booking_id}` - Cancel booking

### Reviews
- `POST /api/V1/reviews/` - Create review
- `GET /api/V1/reviews/` - Get all reviews
- `GET /api/V1/reviews/{review_id}` - Get review details
- `PUT /api/V1/reviews/{review_id}` - Update review
- `DELETE /api/V1/reviews/{review_id}` - Delete review

## 🔧 Database Models

### Core Entities

- **User**: Authentication and user information
- **Theater**: Theater/venue information
- **Screen**: Individual screens within theaters
- **Seat**: Seats within screens
- **Movie**: Movie information and metadata
- **Showtime**: Scheduled movie screenings
- **Booking**: Customer bookings
- **Booking_Seat**: Seat reservations within bookings
- **Payment**: Payment transactions
- **Review**: Movie and theater reviews

### Enums

- **UserRole**: CUSTOMER, THEATER_MANAGER, ADMIN
- **SeatType**: STANDARD, PREMIUM, VIP, ACCESSIBLE
- **ScreenType**: STANDARD, IMAX, DOLBY_CINEMA, 3D, 4DX
- **MovieStatus**: UPCOMING, NOW_SHOWING, ENDED
- **ShowtimeStatus**: SCHEDULED, CANCELLED, COMPLETED, SOLD_OUT
- **BookingStatus**: PENDING, PAYMENT_PENDING, CONFIRMED, CANCELLED, REFUNDED, COMPLETED
- **PaymentStatus**: PENDING, PROCESSING, COMPLETED, FAILED, REFUNDED, CANCELLED
- **Rating**: G, PG, PG-13, R, NC-17

## 🔨 Development

### Running Tests
```
bash
# Add test dependencies and run tests
pytest
```

### Creating Migrations
```
bash
# Create a new migration
alembic revision --autogenerate -m "migration message"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Code Style
The project follows standard Python conventions and uses:
- Type hints for better code documentation
- SQLModel for type-safe database operations
- Pydantic for request/response validation

## 📝 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DataBase_Url` | PostgreSQL connection URL | Required |
| `secret_key` | JWT signing key | Required |
| `Algorithm` | JWT algorithm | HS256 |
| `Expire_ACCESS_TOKEN` | Access token expiry (minutes) | 3 |
| `Expire_Refresh_TOKEN` | Refresh token expiry (days) | 7 |

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

- **Zain Ali** - Initial work

## 🙏 Acknowledgments

- FastAPI team for the amazing framework
- SQLModel for simplifying SQLAlchemy usage
- All contributors and supporters

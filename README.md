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
5. **Configure environment variables**
   
   Edit `compose.yaml` file:
   
```
postgressContainer envirnment:
   username:
   password
   database_name"
   
   
```


1. **Using Docker Compose**
   
```
bash
   docker-compose up --build
   
```
2. **Access the API documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

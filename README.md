# 🚖 Inter-City Cab Management Portal  

This project is an **admin and booking tool** for managing inter-city cabs. It enables **cab registration, location update, booking assignments, and cab state management** using a state machine.

---

## 📌 Features  

### 🔹 Core Functionalities  
- **Cab Registration** – Add new cabs to the system.  
- **City Management** – Onboard various cities where cabs operate.  
- **Location Update** – Change the current city of any cab.  
- **State Management** – Manage cab states (e.g., `IDLE`, `ON_TRIP`).  
- **Cab Booking** – Assign cabs based on availability using the following logic:
  1. Assign the **most idle cab** in the requested city.  
  2. If multiple cabs have been idle for the same duration, assign **randomly**.  
  3. **No cancellations** once assigned.  

### 🔹 Bonus Features  
- **Cab Idle Time Tracking** – Calculate how long a cab has been idle in a given duration.  
- **Cab History Tracking** – Maintain a record of all state transitions for each cab.  
- **Demand Analytics** – Identify high-demand cities and peak booking hours.  

---

## 🛠️ Tech Stack  
- **Backend:** FastAPI  
- **Database:** PostgreSQL
- **Containerization:** Docker  
- **Testing:** Pytest  

---

## 📦 Project Structure  
```
intercity-cab-management/
├── app/
│   ├── __init__.py
│   ├── main.py  # FastAPI entry point
│   ├── models.py  # SQLAlchemy models
│   ├── schemas.py  # Pydantic schemas
│   ├── database.py  # Database connection setup
│   ├── state_machine.py  # IDLE, ON_TRIP etc. 
│   ├── config.py  # App configuration
│   ├── services/
│   │   ├── __init__.py
│   │   ├── cab_service.py  # Cab-related logic
│   │   ├── booking_service.py  # Booking logic
│   │   ├── city_service.py  # City-related logic
│   │   ├── analytics_service.py  # Demand analytics logic
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── cab_repository.py  # Data access for cabs
│   │   ├── booking_repository.py  # Data access for bookings
│   │   ├── city_repository.py  # Data access for cities
│   ├── api/
│   │   ├── __init__.py
│   │   ├── cab_routes.py  # Cab API endpoints
│   │   ├── booking_routes.py  # Booking API endpoints
│   │   ├── city_routes.py  # City API endpoints
│   │   ├── analytics_routes.py  # Analytics API endpoints
│   ├── utils/
│   │   ├── __init__.py
│
├── tests/
│   ├── test_cabs.py  # Unit tests for cabs
│   ├── test_bookings.py  # Unit tests for bookings
│   ├── test_cities.py  # Unit tests for cities
│   ├── test_analytics.py  # Unit tests for analytics
│
├── coverage_report/
│    ├── index.html
│    ├── *.html
├── requirements.txt  # Dependencies
├── Dockerfile  # Containerization setup
├── eval.Dockerfile  # Containerization setup for test
├── docker-compose.yml  # Containerization setup
├── Docdocker-compose.eval.ymlkerfile  # Containerization setup for test
├── .env  # Environment variables
├── README.md  # Project documentation
├── eval.sh  # Run test cases
├── local_run.sh  # run locally
├── README.md  # stop running containers
```

---

## Prerequisites  

- Docker installed on your system  

---


## Run/Debug/Develop Locally
```bash
chmod +x local_run.sh
./local_run.sh
```

## Stop locally
```bash
chmod +x stop.sh
./stop.sh
```


## Evaluate Test cases
```bash
chmod +x eval.sh
./eval.sh
```

## Test coverage
```bash
intercity-cab-management/coverage_report/index.html
```

## Api Documentation
```bash
http://localhost:8000/docs
```

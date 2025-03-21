from fastapi import FastAPI
from app.api import cab_routes, booking_routes, city_routes, analytics_routes
from app.database import Base, engine

print("Creating tables...")
Base.metadata.create_all(bind=engine, checkfirst=True)
print("Tables created.")


app = FastAPI(
    title="Intercity Cab Management API",
    openapi_tags=[
        {"name": "Cities", "description": "Manage city-related operations"},
        {"name": "Cabs", "description": "Manage cabs and their states"},
        {"name": "Bookings", "description": "Handle booking requests"},
        {"name": "Analytics", "description": "View cab demand and history"}
    ]
)


@app.get("/", tags=['Root'])
def root():
    return {
        "message": "Welcome to Intercity Cab API",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "api_version": "1.0.0"
    }


# Register Routers
app.include_router(city_routes.router)
app.include_router(cab_routes.router)
app.include_router(booking_routes.router)
app.include_router(analytics_routes.router)


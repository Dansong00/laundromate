from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config.settings import settings
from app.auth.router import router as auth_router
from app.customers.router import router as customers_router
from app.orders.router import router as orders_router
from app.notifications.router import router as notifications_router
from app.core.database.migrate import create_all_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting LaundroMate API...")
    try:
        if settings.ENV == "development":
            print("🔧 Development mode: Creating database tables...")
            create_all_tables()
            print("✅ Database tables created/updated successfully!")
        else:
            print("🏭 Production mode: Skipping auto table creation")
    except Exception as e:
        print(f"⚠️  Warning: Could not create tables: {e}")
        # Don't crash the app on startup

    yield

    # Shutdown
    print("🛑 Shutting down LaundroMate API...")


app = FastAPI(
    title="LaundroMate API",
    description="Modern SaaS platform for full-service laundromats",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(customers_router, prefix="/customers", tags=["Customers"])
app.include_router(orders_router, prefix="/orders", tags=["Orders"])
app.include_router(notifications_router, prefix="/notifications", tags=["Notifications"])


@app.get("/")
async def root():
    return {"message": "Welcome to LaundroMate API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

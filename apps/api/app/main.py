from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config.settings import settings
from app.auth.router import router as auth_router
from app.customers.router import router as customers_router
from app.orders.router import router as orders_router
from app.notifications.router import router as notifications_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting LaundroMate API...")
    print("🔒 Database tables must be created via Alembic migrations")
    print("📚 Run 'alembic upgrade head' to apply pending migrations")

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

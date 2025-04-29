from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager

from app.game_progress import router as progress_router

try:
    from app import models, database, users, quizzes, seed
except ImportError:
    import app.models as models
    import app.database as database
    import app.users as users
    import app.quizzes as quizzes
    import app.seed as seed
# Create all tables
models.Base.metadata.create_all(bind=database.engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Seed the database
    print("Seeding the database...")
    seed.seed_data()
    seed.upload_neoverse_logs()  # Calls your seeding function
    yield
    # Shutdown: add any cleanup code here if needed

app = FastAPI(lifespan=lifespan)

# Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:80",
        "http://localhost:443",
        "http://localhost",
        "http://10.0.0.12",         # Frontend EC2 instance private IP
        "http://10.0.0.12:3000",    # In case you're using a specific port
        "http://10.0.0.12:5173",    # If using Vite's default port
        "http://10.0.0.12:80",      # Standard HTTP port
        "http://10.0.0.12:443"      # HTTPS port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}


app.include_router(users.router)
app.include_router(quizzes.router)
app.include_router(progress_router)

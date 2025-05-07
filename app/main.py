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
    allow_origins=["*"],  # Allow all origins
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

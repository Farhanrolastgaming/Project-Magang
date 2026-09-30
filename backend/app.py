from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import engine, Base
from routes import auth_routes

# Create DB Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gen-AutoPress Platform API")

# Configure CORS for Next.js frontend communication
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
from routes import auth_routes, wp_routes, admin_routes

app.include_router(auth_routes.router, prefix="/api/auth", tags=["auth"])
app.include_router(wp_routes.router, prefix="/api/wp", tags=["wp"])
app.include_router(admin_routes.router, prefix="/api/admin", tags=["admin"])

@app.get("/api/health")
def read_root():
    return {"status": "Gen-AutoPress API is running"}

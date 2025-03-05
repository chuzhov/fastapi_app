
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal, engine
from app.security import get_password_hash
import uvicorn

from datetime import datetime

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
        <html>
            <head>
                <title>Welcome</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 40px;
                        text-align: center;
                    }
                    h1 {
                        color: #333;
                    }
                </style>
            </head>
            <body>
                <h1>Welcome to My FastAPI App</h1>
                <p>This is a simple HTML response.</p>
            </body>
        </html>
    """

@app.get("/health")
def health_check():
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "timestamp": datetime.now().isoformat()
        }
    )


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user with this email exists
    db_user = db.query(models.User) \
                .filter(models.User.email == user.email) \
                .first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username is taken
    db_user = db.query(models.User) \
                .filter(models.User.username == user.username) \
                .first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3000)
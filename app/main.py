from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from datetime import datetime

app = FastAPI()

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

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3000)
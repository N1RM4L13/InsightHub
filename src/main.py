import uvicorn
from src.api.app import app  # Import FastAPI app from api/app.py

# Run the application with Uvicorn if main.py is run directly
if __name__ == "__main__":
    uvicorn.run("src.api.app:app", host="127.0.0.1", port=8000, reload=True)

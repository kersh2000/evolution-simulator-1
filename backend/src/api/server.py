import os
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
async def read_root():
    # Construct the absolute path
    path = os.path.join(os.path.dirname(__file__), 'templates', 'home.html')
    return FileResponse(path)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv('SERVER_PORT', 8000))  # Default to port 8000 if not specified
    uvicorn.run(app, host="localhost", port=port)

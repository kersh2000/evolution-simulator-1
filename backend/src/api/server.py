import sys
sys.dont_write_bytecode = True

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse

from ..db.models import models
from ..db.db import engine

from .routers import routers


load_dotenv('.env')

# Creates all of the models for our database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routers.authRouter)
app.include_router(routers.userRouter)
app.include_router(routers.simulationRouter)
app.include_router(routers.blockRouter)

@app.get("/")
async def read_root():
    # Construct the absolute path
    path = os.path.join(os.path.dirname(__file__), 'templates', 'home.html')
    return FileResponse(path)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv('SERVER_PORT', 8000))  # Default to port 8000 if not specified
    uvicorn.run(app, host="localhost", port=port)

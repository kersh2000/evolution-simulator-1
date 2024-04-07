import sys
sys.dont_write_bytecode = True

import os
from fastapi import FastAPI
from fastapi.responses import FileResponse

from ..db.models import models
from ..db.db import engine
from ..config import server_port
from .routers import routers

# Creates all of the models for our database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routers.authRouter)
app.include_router(routers.userRouter)
app.include_router(routers.simulationRouter)
app.include_router(routers.blockRouter)
app.include_router(routers.environmentRouter)

@app.get("/")
async def read_root():
    # Construct the absolute path
    path = os.path.join(os.path.dirname(__file__), 'templates', 'home.html')
    return FileResponse(path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=server_port)

import sys
from typing import Dict
sys.dont_write_bytecode = True

import os
from fastapi import FastAPI
from fastapi.responses import FileResponse

# from ..db.models import models
# from ..db.db import engine

from ..code import simulation
from ..code.classes.block import Block
from fastapi.middleware.cors import CORSMiddleware

# Creates all of the models for our database
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORSMiddleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def read_root():
    # Construct the absolute path
    path = os.path.join(os.path.dirname(__file__), 'templates', 'home.html')
    return FileResponse(path)

@app.get("/code")
async def get_env():
    simulation.begining()
    return {
        "env": simulation.env
    }

@app.post("/step")
async def step(env: Dict):
    simulation.setup(env["env"])
    simulation.step()
    return {
        "env": simulation.env,
        "total_count": simulation.total_concs
    }

@app.post("/step/{num}")
async def step(num: int, env: Dict):
    simulation.setup(env["env"])
    for step in range(num):
        simulation.step()
    return {
        "env": simulation.env,
        "total_count": simulation.total_concs
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

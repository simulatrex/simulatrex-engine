from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from simulatrex.dsl_parser import (
    parse_dsl,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class SimulationRequest(BaseModel):
    code: str


@app.post("/api/v1/simulation")
async def run_simulation(request: SimulationRequest):
    try:
        simulation = parse_dsl(request.code)
        if simulation:
            await simulation.run()  # Ensure this is awaited
            return {"status": "Simulation completed successfully."}
        else:
            return {"status": "No simulation found in the DSL code."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

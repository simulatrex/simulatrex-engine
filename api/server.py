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
        print(request.code)
        # Parse the DSL code
        simulation_data = parse_dsl(request.code)

        print(simulation_data)
        # Run the simulation with your simulation engine
        # For now, we'll just return the parsed data

        return simulation_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

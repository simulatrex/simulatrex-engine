import asyncio
import json
import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from openai import OpenAI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import logging

from simulatrex.dsl_parser import (
    parse_dsl,
)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all originsas needed
    allow_credentials=True,
    allow_methods=["*"],  # Or specify just the methods you need: ["GET", "POST"]
    allow_headers=["*"],  # Or specify just the headers you need
)


class SimulationRequest(BaseModel):
    code: str


simulation_task: asyncio.Task = None
progress = 0
simulation_logs = []

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("simulation_logger")


class StreamLogHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        simulation_logs.append(
            log_entry
        )  # Assuming simulation_logs is your global list


# Add the custom handler to the logger
logger.addHandler(StreamLogHandler())


@app.post("/api/v1/simulation")
async def run_simulation(request: SimulationRequest):
    global simulation_task

    if simulation_task and not simulation_task.done():
        raise HTTPException(status_code=400, detail="Simulation is already running")

    if not request.code:
        raise HTTPException(status_code=400, detail="DSL code is required.")

    try:
        simulation = parse_dsl(request.code)
        agents = [agent.to_dict() for agent in simulation.agents]
        environment = simulation.environment.to_dict()
        simulation_details = simulation.to_dict()
        if simulation:
            simulation_task = asyncio.create_task(simulation.run())
            return {
                "status": "Simulation started successfully.",
                "simulation": simulation_details,
                "agents": agents,
                "environment": environment,
            }
        else:
            return {"status": "No simulation found in the DSL code."}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@app.route("/api/v1/simulation/stream")
def stream_simulation_progress(request: Request):
    def generate():
        global progress, simulation_logs
        simulation_logs.clear()
        while True:
            data = {"progress": progress, "logs": simulation_logs}
            yield f"data: {json.dumps(data)}\n\n"

            time.sleep(1)  # Adjust the sleep time as needed

    response = StreamingResponse(generate(), media_type="text/event-stream")
    response.headers["Access-Control-Allow-Origin"] = "*"  # For testing purposes
    return response


@app.post("/api/v1/simulation/cancel")
async def cancel_simulation():
    global simulation_task
    global progress
    global simulation_logs

    if simulation_task and not simulation_task.done():
        simulation_task.cancel()
        simulation_logs.clear()
        print("Simulation cancelled successfully.")
        progress = 0
        try:
            await simulation_task
        except asyncio.CancelledError:
            pass  # Task cancellation is expected
        finally:
            simulation_task = None
        return {"message": "Simulation cancelled and reset successfully."}
    else:
        return {"message": "No simulation is running to cancel."}


class ImageGenerationRequest(BaseModel):
    description: str


@app.get("/api/v1/preview/generate")
def generate_image(description: str = ""):
    client = OpenAI()

    if not description:
        raise HTTPException(status_code=400, detail="Description is required.")

    try:
        response = client.images.generate(
            model="dall-e-3", prompt=description, n=1, size="512x512"
        )
        if response.data:
            image_url = response.data[0].url
        else:
            image_url = None

        print("Image URL", image_url)
        return {
            "status": "Image generated successfully.",
            "image_url": image_url,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    app.run(debug=True)

import asyncio
import dotenv
from simulatrex import SimulationEngine

dotenv.load_dotenv()


async def main():
    engine = SimulationEngine(config_path="./data/3_crisis_management_simulation.json")
    await engine.run()


if __name__ == "__main__":
    asyncio.run(main())

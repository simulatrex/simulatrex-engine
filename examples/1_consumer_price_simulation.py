import asyncio
import dotenv
from simulatrex import SimulationEngine

dotenv.load_dotenv()


async def main():
    engine = SimulationEngine(
        config_path="./data/1_consumer_price_simulation_config.json"
    )
    await engine.run()


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import dotenv
from simulatrex import SimulationEngine

dotenv.load_dotenv()


async def main():
    engine = SimulationEngine("./data/2_policy_impact_local_communities.json")
    await engine.run()


if __name__ == "__main__":
    asyncio.run(main())

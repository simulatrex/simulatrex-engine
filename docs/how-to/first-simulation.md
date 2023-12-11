# Running Your First Simulation

To run your first simulation, you need to follow these steps:

1. Import the `SimulationEngine` from the `simulatrex` package.
2. Create an instance of the `SimulationEngine`, passing the simulation configuration as a parameter.
3. Run the simulation using the `run` method of the `SimulationEngine`.
4. Get the evaluation data using the `get_evaluation_data` method of the `SimulationEngine`.
5. Convert the evaluation data to a Pandas DataFrame for easier manipulation and analysis.

Here is an example of how to do this:

```python
from simulatrex import SimulationEngine
import pandas as pd

simulation_config = {...}  # Your simulation configuration here

engine = SimulationEngine(config=simulation_config)
await engine.run()
evaluation_data = engine.get_evaluation_data()

df = pd.DataFrame(evaluation_data)
```

Replace `{...}` with your actual simulation configuration, or alternatively reference to a json file.


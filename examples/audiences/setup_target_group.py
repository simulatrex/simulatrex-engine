import dotenv
from simulatrex import TargetGroup

dotenv.load_dotenv()

audience = TargetGroup(id="Early adopters").age_range(25, 40)

print(audience.describe())

import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic data for 500+ companies
n = 520
data = {
    "R&D Spend": np.random.randint(10000, 200000, size=n),
    "Administration": np.random.randint(50000, 180000, size=n),
    "Marketing Spend": np.random.randint(0, 300000, size=n)
}

df = pd.DataFrame(data)
df.to_csv("input_500_companies.csv", index=False)
print("✅ File saved as input_500_companies.csv")

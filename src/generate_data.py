import pandas as pd
import sys
import os

from datetime import datetime

DEFENDERS = ["flutter-mane"]
DEFENDER_SOURCE_PATH = "src/dataset/dataset-draft-3.csv"

sys.path.append(os.getcwd())
abs_path = os.path.abspath(os.getcwd())
defender_stats_path = os.path.join(abs_path, DEFENDER_SOURCE_PATH)
stats_df = pd.read_csv(defender_stats_path)

data = []
for d in DEFENDERS:
    stats = stats_df[stats_df['defender'] == d].iloc[0]
    for b4 in range(8000, 16000, 100):
        for b5 in range(12000, 22000, 100):
            data.append({'b1': stats['b1'],
                         'b2': stats['b2'],
                         'b3': stats['b3'],
                         'b4': b4,
                         'b5': b5,
                         'attacker': 'generated',
                         'defender': d})

df = pd.DataFrame(data)
date_time = datetime.now().strftime("%m_%d_%H_%M_%S")
df.to_csv(f"src/dataset/generated_data_{date_time}.csv")

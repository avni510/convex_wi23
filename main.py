from pathlib import Path
import dill
import pandas as pd
import sys
import os
from src import executor
sys.path.append(os.getcwd())

OPTIONS = ['MIQCP', 'BASELINE', 'CLOSED_FORM']
to_run = OPTIONS[1]
abs_path = os.path.abspath(os.getcwd())
data = abs_path + "/src/dataset/generated_data_traditional_03_21_11_48_41.csv"

df = pd.read_csv(data)
bs = df[["b1", "b2", "b3", "b4", "b5"]].to_numpy()
attackers = df["attacker"].to_numpy()
defenders = df["defender"].to_numpy()
if to_run == OPTIONS[0]: 
    results = executor.run(bs, attackers, defenders) 
elif to_run == OPTIONS[1]:
    results = executor.run_baseline(bs, attackers, defenders) 
else: 
    results = executor.run_closed_form(bs, attackers, defenders)

f = Path(abs_path + "/results/results_generated_"+to_run+".pkl")

with open(f, 'wb') as outfile:
    dill.dump(results, outfile, protocol=dill.HIGHEST_PROTOCOL)

## check it's saved correctly
with open(f, 'rb') as infile:
    file_contents = dill.load(infile)

assert len(results) == len(file_contents)

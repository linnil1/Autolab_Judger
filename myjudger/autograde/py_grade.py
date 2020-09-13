import json
import sys
import time
import os
from Solution import Solution

# Init
time_limit = 800
samples = json.load(open(sys.argv[1] + ".in"))
need_remove = True
output = {"status": [],
          "time": []}

def run(sample):
    return Solution().solve(sample["a"], sample["b"])


def compare(out, ans):
    return out == ans


if need_remove:
    open(sys.argv[1] + ".in", "w").close()

# Run per sample in this case
for sample in samples["data"]:
    output["time"].append(0)
    output["status"].append("NA")

    try:
        clk_s = time.time()
        out = run(sample)
        # Your Custom method caller
        output["time"][-1] = (time.time() - clk_s) * 1000
    # Maybe can catch Exception
    except Exception as e:
        output["status"][-1] = 'RE'
        continue

    # Your custom answer checker
    # Need to check the out type before comparing
    if compare(out, sample["ans"]):
        output["status"][-1] = 'AC'
    else:
        output["status"][-1] = 'WA'

    # time limit
    if output["time"][-1] > time_limit:
        output["status"][-1] = 'TLE'


# Exit
json.dump(output, open(sys.argv[1] + ".out", 'w'))
sys.exit(0)

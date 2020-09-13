import json
import sys
import time
import os

# -----------------------------------------------
# Custom region
time_limit = 800


def run(sample):
    from Solution import Solution
    return Solution().twoSum(sample['nums'], sample['target'])


def compare(out, sample):
    if type(out) is not list:
        return False
    if len(out) != 2:
        return False
    if type(out[0]) is not int or type(out[1]) is not int:
        return False
    return sample['answer'] == out 
# -----------------------------------------------


# Init
samples = json.load(open(sys.argv[1] + ".in"))
open(sys.argv[1] + ".in", "w").close()
output = {"status": [],
          "time": []}

# Run per sample in this case
for sample in samples:
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
    if compare(out, sample):
        output["status"][-1] = 'AC'
    else:
        output["status"][-1] = 'WA'

    # time limit
    if output["time"][-1] > time_limit:
        output["status"][-1] = 'TLE'


# Exit
json.dump(output, open(sys.argv[1] + ".out", 'w'))
sys.exit(0)

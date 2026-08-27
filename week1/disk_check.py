#disk_check.py - my python version of the disck checker

threshold = 80
print('checking disk usage')

import subprocess
result = subprocess.run(["df","-h"], capture_output=True , text=True)
lines = result.stdout.strip().split("\n")
for line in lines[1:]:
    parts = line.split()
    capacity = None
    mount = parts[-1]
    for item in parts:
        if item.endswith("%"):
            capacity = item
            break
    if capacity  is None:
        continue
    usage = int(capacity.replace("%",""))
    if usage > threshold:
        print(f"Warning: {mount} is {usage}% full" )
print("Done")

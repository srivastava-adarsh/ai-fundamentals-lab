# A simple function
def great(name):
    return f"Hello, {name}!"

#call it
message = great("Adarsh")
print(message)

#Call it again with a different input
print(great("world"))

import subprocess

def check_disk_usage(threshold):
    result = subprocess.run(["df","-h"], capture_output=True, text = True)
    lines = result.stdout.strip().split("\n")
   # print(f"DEBUG: {lines}")
    warnings = []
    for line in lines[1:]:
        parts = line.split()
    #    print(f"DEBUG parts: {parts}")
        mount=parts[-1]
       # print(f"DEBUG Mount - {mount}")
        capacity = None
        for item in parts:
            if item.endswith("%"):
                capacity = item
          #      print(f"DEBSUG capacity - {capacity}")
                break
        if capacity is None:
            continue
        usage = int(capacity.replace("%",""))
    #    print(f" DEBUG: {mount}. ---> {usage}%")
        if usage > threshold:
            warnings.append(f"{mount} is {usage}% full")
    return warnings

#call it with threshold 80
alerts = check_disk_usage(80)
print(f"Found {len(alerts)} filesystems over threshold:")
for alert in alerts:
    print(" -", alert)

#Reuse the same function with a different threshold
print("\nStricter check (threshold 60):")
strict_alerts = check_disk_usage(60)
for alert in strict_alerts:
    print(" -", alert)






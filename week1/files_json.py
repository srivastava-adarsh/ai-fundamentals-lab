#Part 1: Reading and Writing a plain text file

#Write a file
with open("notes.txt", "w") as f:
    f.write("First Line\n")
    f.write("Second line\n")

#Read it back
with open("notes.txt", "r") as f:
    content = f.read()

print("File contents:")
print(content)


#Part 2: JSON - the format APIs use

import json

#A python dict
config = {
    "model": "auto",
    "temperature": 0.7,
    "max_retries": 3
}

#Write down the dict to json files
with open("config.json", "w") as f:
    json.dump(config,f, indent=2)

print("wrote config.json")

with open("config.json", "r") as f:
    loaded = json.load(f)

print("Loaded config:" , loaded)
print("Model is:", loaded["model"])

loaded["temperature"] = 0.2
loaded["max_retries"] = 5

with open("config.json", "w") as f:
    json.dump(loaded, f, indent=2)

print("updated config saved")

#Verify by reading again
with open("config.json", "r") as f:
    final = json.load(f)

print("final config:", final)

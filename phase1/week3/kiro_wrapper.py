import subprocess
import re

def clean_output(raw):
    #Remove color ANSI codes
    ansi_pattern = re.compile(r"\x1b\[[0-9;]*m")
    cleaned = ansi_pattern.sub("", raw)
    cleaned = cleaned.strip()

    #remove the leading ">"
    if cleaned.startswith("> "):
        cleaned = cleaned[2:]

    return cleaned.strip()

def ask_llm(prompt):
    try:
        result = subprocess.run(
            ["kiro-cli","chat","--no-interactive", "--model", "auto", prompt],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        return "Error: Kiro took too long to respond"

    if result.returncode != 0:
        return f"ERROR: Kiro failed (exit code {result.returncode}):  {result.stderr.strip()}"

    cleaned = clean_output(result.stdout)
    if not cleaned:
        return "ERROR: Kiro returned an empty response"

    return cleaned

import json

def ask_llm_json(prompt):
    #Instruct the model to return only valid JSON
    full_prompt = ( prompt + "\n\nRespond only with valid JSON, no markdown, no code fences, no explanation")

    raw = ask_llm(full_prompt)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return{"Error": "model did not return valid JSON" , "raw": raw}

#test it
info = ask_llm_json("Give me info about python language: name, year created, creator. " 
                    "Return JSON with exactly these keys"
                    '"name"(string), "year_created"(integer), "creator" (string).')



if "Error" not in info:
    print(f"{info['name']} was created in {info['year_created']} by {info['creator']}.")
else:
    print("Could not get structured data", info["raw"])


def ask_with_history(messages):
    #Flatten the conversation history into a single prompt
    conversation = ""
    for msg in messages:
        conversation += f"{msg['role']}: {msg['content']}\n"
    conversation += "assistant:"
    return ask_llm(conversation)

#Test: Maintain history ourselves
messages = [{"role": "user" , "content": "My name is Bond, Remmeber it"},]

reply1 = ask_with_history(messages)
print("Assistant: ", reply1)

#add the assitant's reply to history, then ask again
messages.append({"role":"assistant", "content":reply1})
messages.append({"role":"user", "content":" What is my name?"})

reply2 = ask_with_history(messages)
print("Assistant: ", reply2)


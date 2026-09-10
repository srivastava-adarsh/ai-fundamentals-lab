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
    except subprocess.Timeout.Expired:
        return "Error: Kiro took too long to respond"

    if result.returncode != 0:
        return f"ERROR: Kiro failed (exit code {result.returncode}):  {result.stderr.strip()}"

    cleaned = clean_output(result.stdout)
    if not cleaned:
        return "ERROR: Kiro returned an empty response"

    return cleaned


#Test it
reply = ask_llm("In one sentence, what is a REST API")
print(reply)
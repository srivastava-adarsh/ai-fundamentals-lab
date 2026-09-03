import requests

url = "https://jsonplaceholder.typicode.com/users/1"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status() #raises an error 

    data = response.json()
    print("Name:", data["name"])
    print("Email:", data["email"])
    print("City:", data["address"]["city"])

except requests.exceptions.Timeout:
    print("Error: The request timed out")
except requests.exceptions.HTTPError as e:
    print(f"Error: HTTP error - {e}")
except requests.exceptions.RequestException as e:
    print(f"ERROR: The exception is {e}")

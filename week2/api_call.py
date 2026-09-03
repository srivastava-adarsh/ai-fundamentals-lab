import requests

#Call a free public API ( no key needed) - a test API that retruns fake JSON data 
response=requests.get("https://jsonplaceholder.typicode.com/users/1")

print("Status code:", response.status_code)
print("Raw text: ", response.text)

#lists n- ordered collections

fruits = ["apple", "banana", "cherry"]
print(fruits)
print(fruits[0])
print(len(fruits))

#Modifying lists
fruits.append("date")
print(fruits)

#looping with pisition
for i,fruit in enumerate(fruits):
    print(i,fruit)

#Dictionaries: key-value pairs
message= {"role":"user", "content":"Hello,How are you?"}
print(message)
print(message["role"])
print(message["content"])

conversation = [
    {"role": "system", "content": "You are a helpful assistant" },
    {"role" : "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language"}
]

print("Number of messages:", len(conversation) )

for msg in conversation:
    print(f"[{msg['role']}] {msg['content']}")
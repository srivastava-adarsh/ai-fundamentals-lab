def divide(a,b):
    try: 
        return a/b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero")
        return None
    except TypeError:
        print("Error: Both inputs must be numbers")
        return None

    
#Test several cases
print("10.0/2 =  ", divide(10,2))
print("10.0/0 =  ", divide(10,0))
print("10 / 'x' =", divide(10, "x"))

print("Program finished successfully")


#finally always runs, success or failure
def read_config(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"config '{filename}' not found - using defaults")
        return "default config"
    finally:
        print("(config lookup attempt complete)")

print("\nTrying existing files")
print(read_config(".env"))


print("\nTrying missing file")
print(read_config("nonexistent.txt"))


def announce(f):
    def wrapper():
        print("About to run the function...")
        f()
        print("Done with the function")
    return wrapper

@announce # decorator
def hello():
    print("Hello, world!")

hello()

"""
python decorators.py
->About to run the function...
->Hello, world!
->Done with the function
"""
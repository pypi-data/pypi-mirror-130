def greeting():
    """function to greet the user"""
    name = input('hello! what your name? \n').capitalize()
    welcome = print(f"Welcome {name}")
    return welcome 
if __name__ == '__main__':
    greeting()

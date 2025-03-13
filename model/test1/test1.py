import os

def test1():
    my_path = os.path.dirname(os.path.abspath(__file__))
    print(my_path)


class Adaptee:
    def specific_request(self):
        return 'Adaptee'


class Adapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def request(self):
        return self.adaptee.specific_request()

client = Adapter(Adaptee())
print(client.request())

# --------- Second example (by Alex Martelli)------------

class UppercasingFile:
    def __init__(self, *a, **k):
        self.f = open(*a, **k)

    def write(self, data):
        self.f.write(data.upper())

    def __getattr__(self, name):
        return getattr(self.f, name)

# usage
import os


print("current working directory: " + os.getcwd())
print(os.path.dirname(os.path.realpath(__file__)))

upper_file = UppercasingFile('test.txt', encoding='utf-8', mode='w+')
upper_file.write("hello world of adapter :)")
print(os.path.abspath('test.txt'))

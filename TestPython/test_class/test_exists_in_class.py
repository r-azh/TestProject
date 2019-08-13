__author__ = 'R.Azh'


class Containers:
    wall = "walls"
    group = "groups"
    company = "companies"

container = Containers.wall

if container in Containers.__dict__.values():
    print('exists in class')

container2 = 'walls'

if container2 in Containers.__dict__.values():
    print('exists in class')




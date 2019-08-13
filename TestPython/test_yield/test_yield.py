__author__ = 'R.Azh'

x = [1, 2, 3]


def y():
    for i in x:
        yield i
        print(i)

for j in y():
    print('i : ', str(j))

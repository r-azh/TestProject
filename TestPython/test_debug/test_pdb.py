__author__ = 'R.Azh'

import pdb

def test_module():
    import pdb; pdb.set_trace()
    str1 = 'hi'
    print(str1)

    str2 = 'well hello'
    print(str2)
    a = 10
    b = 100
    c = a + b
    print(c)

pdb.run('test_module()')

# print s for step
# print n for next
# c continue to next breakpointa
# p str1 to print its value


# or in command
# python -m pdb test_pdb.py

# import pdb; pdb.Pdb(skip=['django.*']).set_trace()

__author__ = 'R.Azh'
# http://www.ibm.com/developerworks/library/l-prog/

# Normal statement-based flow control
# if <cond1>:   func1()
# elif <cond2>: func2()
# else:         func3()

# Equivalent "short circuit" expression
# (<cond1> and func1()) or (<cond2> and func2()) or (func3())


x = 3


def pr(s): print(s)

# if x == 1:
#     pr('one')
# elif x == 2:
#     pr('two')
# else:
#     pr('other')

(x == 1 and pr('one')) or (x == 2 and pr('two')) or pr('other')
print('\n')
x = 2
(x == 1 and pr('one')) or (x == 2 and pr('two')) or pr('other')  # don't work properly :(

print('############ using lambda #################')


pri = lambda s: print(s)


namenum = lambda x: (x == 1 and pr("one")) \
                    or (x == 2 and pr("two")) \
                    or (pr("other"))

namenum(1)
print('\n')
namenum(2)
print('\n')
namenum(3)


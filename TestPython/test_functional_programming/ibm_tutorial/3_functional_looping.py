from distlib.compat import raw_input

___author__ = 'R.Azh'

lst = [1, 2, 3, 4, 5]

def func(x): print(x*2)


for e in lst: func(e)

print("################# functional way using map ####################")
list(map(func, lst))

print("################# Map-based action sequence ####################")

do_it = lambda f: f()

f1 = lambda: print("f1: hallo")
f2 = lambda: print("f2: guten morgen")
f3 = lambda: print("f3: gutan tag")

list(map(do_it, [f1, f2, f3]))


# In general, the whole of our main program can be a map() expression with a list of functions to
# execute to complete the program. Another handy feature of first class functions is that you can put them in a list.

print("################# Functional 'while' looping ####################")

# statement-based while loop
# while <cond>:
#     <pre-suite>
#     if <break_condition>:
#         breakelse:
#         <suite>
#
# # FP-style recursive while loop
# def while_block():
#     <pre-suite>
#     if <break_condition>:
#         return 1
#     else:
#         <suite>
#     return 0
#
# while_FP = lambda: (<cond> and while_block()) or while_FP()
# while_FP()


print('###### imperative version of "echo()" ######')
def echo_IMP():
    while 1:
        x = raw_input("IMP (write something) -- ")
        if x == 'quit':
            break
        else:
            print(x)
echo_IMP()

# utility function for "identity with side-effect"
def monadic_print(x):
    print(x)
    return x

print('###### FP version of "echo()" #####')
echo_FP = lambda: monadic_print(raw_input("FP (write something) -- "))=='quit' or echo_FP()
echo_FP()
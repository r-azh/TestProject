__author__ = 'R.Azh'

# Essentially, there are three different kinds of loops:
#
# Count-controlled loops :
# A construction for repeating a loop a certain number of times. An example of this kind of loop is the for-loop of the
# programming language C:
# for (i=0; i <= n; i++)
# Python doesn't know this kind of loop.

# Condition-controlled loop
# A loop will be repeated until a given condition changes, i.e. changes from True to False or from False to True,
#  depending on the kind of loop. There are while loops and do while loops with this behaviour.

# Collection-controlled loop
# This is a special construct which allow looping through the elements of a "collection", which can be an array,
# list or other ordered sequence. Like the for loop of the bash shell (e.g. for i in *, do echo $i; done) or
# the foreach loop of Perl.

# Python supplies two different kinds of loops: the while loop and the for loop, which correspond to the
# condition-controlled loop and collection-controlled loop.

import random
n = 5
to_be_guessed = int(n * random.random()) + 1
guess = 0
while guess != to_be_guessed:
    guess = int(input("New number: "))
    if guess > 0:
        if guess > to_be_guessed:
            print("Number too large")
        elif guess < to_be_guessed:
            print("Number too small")
    else:
        print("Sorry that you're giving up!")
        break
else:
    print("Congratulation. You made it!")
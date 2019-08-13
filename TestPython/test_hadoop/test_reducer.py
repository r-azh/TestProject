__author__ = 'R.Azh'

#!/usr/bin/env python  # for centos
#!/usr/bin/python  # for ubuntu

# chmod +x path/to/reducer.py


from operator import itemgetter
import sys

current_word = None
current_count = 0
word = None

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    word, count = line.split('\t', 1)

    # convert count (currently a string) to int
    try:
        count = int(count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_word == word:
        current_count += count
    else:
        if current_word:
            # write result to STDOUT
            print('%s\t%s' % (current_word, current_count))
        current_count = count
        current_word = word

# do not forget to output the last word if needed!
if current_word == word:
    print('%s\t%s' % (current_word, current_count))


# echo -e  "foo 1\n foo 1\n quux 1\n labs 1\n foo 1\n bar 1\n quux 1\n" | my_python_tests/reducer.py    #dont work

# printf "foo\t1\n foo\t1\n quux\t1\n labs\t1\n foo\t1\n bar\t1\n quux\t1\n" | my_python_tests/reducer.py

# give mapper output to reducer as input
# echo "foo foo quux labs foo bar quux" | /usr/local/hadoop/my_python_test/test_mapper2.py | /usr/local/hadoop/my_python_test/test_reducer2.py



__author__ = 'R.Azh'
#!/usr/bin/env python  # for centos
#!/usr/bin/python  # for ubuntu


# chmod +x path/to/mapper.py

import sys

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    words = line.split()
    # increase counters
    for word in words:
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
        #
        # tab-delimited; the trivial word count is 1
        print('%s\t%s' % (word, 1))


# to test:
# echo "foo foo quux labs foo bar quux" | /usr/local/hadoop/my_python_test/mapper.py

# cat /tmp/gutenberg/20417-8.txt | /home/hduser/mapper.py

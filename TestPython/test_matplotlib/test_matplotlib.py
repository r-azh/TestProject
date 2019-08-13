from TestPython.machine_learning_with_python.utils import CHART_DIR

__author__ = 'R.Azh'
# http://matplotlib.org/users/pyplot_tutorial.html

# matplotlib contains the pyplot package, which tries to mimic MATLAB's
# interface, which is a very convenient and easy to use

# If it doesnt show the figure It could be a problem with the backend. What is the output of
#  python -c 'import matplotlib; import matplotlib.pyplot; print(matplotlib.backends.backend)'?
# If it is the 'agg' backend, what you see is the expected behaviour as it is a non-interactive backend that does not
# show anything to the screen, but work with plt.savefig(...). You should switch to, e.g., TkAgg or Qt4Agg to be able
# to use show. You can do it in the matplotlib.rc file. use code below before importing matplotlib.pyplot
# import matplotlib
# Force matplotlib to not use any Xwindows backend.
# matplotlib.use('Agg')
# matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4])
plt.ylabel('some numbers')
plt.show()
# plt.savefig('test.png')

# import pylab
# pylab.show()

x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
y = [10, 50, 70, 90, 80, 30, 40, 56, 79, 34, 55, 12]

# plot the (x,y) points with dots of size 10
plt.scatter(x, y, s=10)
plt.title("Web traffic over the last month")
plt.xlabel("Time")
plt.ylabel("Hits/hour")
plt.xticks([w*7*24 for w in range(10)], ['week %i' % w for w in range(10)])
plt.autoscale(tight=True)
# draw a slightly opaque, dashed grid
plt.grid(True, linestyle='-', color='0.75')
plt.show()
# plt.savefig('test1.png')




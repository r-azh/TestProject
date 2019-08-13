import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

__author__ = 'R.Azh'

data = sp.genfromtxt(fname="../book/data/web_traffic.tsv", delimiter="\t")
# or
# print(DATA_DIR)
# data = sp.genfromtxt(os.path.join(DATA_DIR, "web_traffic.tsv"), delimiter="\t")
print(data[:10])
print(data.shape)

print("########## Preprocessing and cleaning the data ############")
# separate the dimensions into two vectors
x = data[:, 0]  # hours
y = data[:, 1]  # Web hits in that particular hour

# count of invalid data in y
invalid_data_count = sp.sum(sp.isnan(y))
print(invalid_data_count)

# we are missing only 8 out of 743 entries, so we can afford to remove them.
x = x[~sp.isnan(y)]
y = y[~sp.isnan(y)]

plt.scatter(x, y, s=10)
plt.title("Web traffic over the last month")
plt.xlabel("Time")
plt.ylabel("Hits/hour")
plt.xticks([w*7*24 for w in range(10)], ['week %i' % w for w in range(10)])
plt.autoscale(tight=True)
# draw a slightly opaque, dashed grid
plt.grid(True, linestyle='-', color='0.75')
# plt.show()
# plt.savefig('{}/show_data.png'.format(CHART_DIR))


def error(f, x, y):
    return sp.sum((f(x) - y) ** 2)


print('########## straight line model(polynomial of degree 1) ##########')
fp1, residuals, rank, sv, rcond = sp.polyfit(x, y, 1, full=True)
print("Model parameters: %s" %fp1) # [  2.59619213 989.02487106]
print(residuals) # this is error of approximation :[3.17389767e+08]

# so the best straight line fit is the following function
# f(x) = 2.59619213 * x + 989.02487106
f1 = sp.poly1d(fp1)
print(error(f1, x, y))

fx = sp.linspace(0, x[-1], 1000)  # generate X-values for plotting
plt.plot(fx, f1(fx), linewidth=4)
plt.legend(["d=%i" % f1.order], loc="upper left")
# plt.show()

print('########## polynomial of degree 2 model ##########')
f2p = sp.polyfit(x, y, 2)
print(f2p)
# so the best degree 2 fit is the following function
# f(x) = 0.0105322215 * x**2 - 5.26545650 * x + 1974.76082
f2 = sp.poly1d(f2p)
print(error(f2, x, y))

plt.plot(fx, f2(fx))
plt.legend(["d=%i" % f1.order, "d=%i" % f2.order], loc="upper left")
# plt.show()

print('########## polynomial of degree 3 model ##########')
f3p = sp.polyfit(x, y, 3)
print(f3p)
f3 = sp.poly1d(f3p)
print(error(f3, x, y))

plt.plot(fx, f3(fx))
plt.legend(['d=%i' % f.order for f in [f1, f2, f3]], loc="upper left")
# plt.show()

print('########## polynomial of degree 10 model ##########')
f10p = sp.polyfit(x, y, 10)
print(f10p)

f10 = sp.poly1d(f10p)
print(error(f10, x, y))

plt.plot(fx, f10(fx))
plt.legend(['d=%i' % f.order for f in [f1, f2, f3, f10]], loc="upper left")
# plt.show()

print('########## polynomial of degree 100 model ##########')
f100p = sp.polyfit(x, y, 100)
print(f100p)    # has an overflow error and gives degree 53 instead

f100 = sp.poly1d(f100p)
print(error(f100, x, y))

plt.plot(fx, f100(fx))
plt.legend(['d=%i' % f.order for f in [f1, f2, f3, f10, f100]], loc="upper left")
# plt.show()

print('########## breaking the data from inflection point ##########')
inflection = int(3.5 * 7 * 24)   # calculate the inflection point in hours
xa = x[:inflection]  # data before the inflection point
ya = y[:inflection]
xb = x[inflection:]     # data after
yb = y[inflection:]

f1a = sp.poly1d(sp.polyfit(xa, ya, 1))
f1b = sp.poly1d(sp.polyfit(xb, yb, 1))

fa_error = error(f1a, xa, ya)
fb_error = error(f1b, xb, yb)
print("Error inflection degree 1=%f" % (fa_error + fb_error))

plt.plot(fx, f1a(fx))
plt.plot(fx, f1b(fx))
# plt.legend(['d=%i' % f.order for f in [f1, f2, f3, f10, f100, f1a, f1b]], loc="upper left")
# plt.show()

f2a = sp.poly1d(sp.polyfit(xa, ya, 2))
f2b = sp.poly1d(sp.polyfit(xb, yb, 2))

fa_error = error(f2a, xa, ya)
fb_error = error(f2b, xb, yb)
print("Error inflection degree 2=%f" % (fa_error + fb_error))

plt.plot(fx, f2a(fx))
plt.plot(fx, f2b(fx))
# plt.show()

print('########## training and testing ##########')
train_percent = 0.7
train_data_index = int(len(xb) * train_percent)

shuffled = sp.random.permutation(list(range(len(xb))))
train = sorted(shuffled[:train_data_index])
test = sorted(shuffled[train_data_index:])
fb2_trained = sp.poly1d(sp.polyfit(xb[train], yb[train], 2))

test_error = error(fb2_trained, xb[test], yb[test])
print("Error from testing trained model: %d" % test_error)

print('########## predict when get to 100000 ##########')
print("fb2_trained = \n%s" % fb2_trained)
result_function = fb2_trained - 100000   # for finding when function result in 100,000
print("fb2_trained - 100,000 = \n%s" % result_function)

# finding the root of result function
reached_max = fsolve(result_function, x0=800)   # 800 is an index greater than len(data): point in future for prediction
print("100,000 hits per hour expected at week %f" % (reached_max/(7*24))[0])
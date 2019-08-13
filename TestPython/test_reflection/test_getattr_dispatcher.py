from datetime import datetime

__author__ = 'R.Azh'

# A common usage pattern of getattr is as a dispatcher.
# or example, if you had a program that could output data in a variety of different formats,
# you could define separate functions for each output format and use a single dispatch function to call the right one.


class Statout:

    @classmethod
    def output_text(cls, data):
        print("text:", data)

    @classmethod
    def output_int(cls, data):
        print("int:", data)

    @classmethod
    def output_float(cls, data):
        print("float:", data)

    @classmethod
    def output_datatime(cls, data):
        print("datetime:", data)


def output(data, format="text"):
    # output_function = getattr(Statout, "output_{}".format(format))  # no default function
    output_function = getattr(Statout, "output_{}".format(format), Statout.output_text) # returns Statout.output_text if doesnt exist
    return output_function(data)


output("hello")
output("nice", "text")
output(123, "int")
output(3.2, "float")
output(datetime.utcnow(), "datatime")
output("wrong format!", "pdf")

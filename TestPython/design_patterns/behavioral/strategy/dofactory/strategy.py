__author__ = 'R.Azh'

# Define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets the algorithm vary
# independently from clients that use it.


# Strategy: declares an interface common to all supported algorithms. Context uses this interface to call the algorithm
# defined by a ConcreteStrategy
class SortStrategy:
    def sort(self, list_to_sort):
        raise NotImplementedError


# ConcreteStrategy: implements the algorithm using the Strategy interface
class QuickSort(SortStrategy):
    def sort(self, list_to_sort):
        print("\n-- quick sort --")
        list_to_sort.sort()
        print("quick sorted list")


class ShellSort(SortStrategy):
    def sort(self, list_to_sort):
        print("\n-- shell sort --")
        self._shell_sort(list_to_sort)
        print("shell sorted list")

    def _shell_sort(self, alist):
        sub_list_count = len(alist)//2
        while sub_list_count > 0:

            for start_position in range(sub_list_count):
                self._gap_insertion_sort(alist, start_position, sub_list_count)

            # print("After increments of size", sub_list_count, "The list is", alist)
            sub_list_count //= 2

    def _gap_insertion_sort(self, alist, start, gap):
        for i in range(start+gap, len(alist), gap):

            current_value = alist[i]
            position = i

            while position >= gap and alist[position-gap] > current_value:
                alist[position] = alist[position-gap]
                position = position-gap

            alist[position] = current_value


class MergeSort(SortStrategy):
    def sort(self, list_to_sort):
        print("\n-- merge sort --")
        self.merge_sort(list_to_sort)
        print("merge sorted list")

    def merge_sort(self, alist):
        # print("Splitting ", alist)
        if len(alist) > 1:
            mid = len(alist)//2
            left_half = alist[:mid]
            right_half = alist[mid:]

            self.merge_sort(left_half)
            self.merge_sort(right_half)

            i, j, k = 0, 0, 0
            while i < len(left_half) and j < len(right_half):
                if left_half[i] < right_half[j]:
                    alist[k] = left_half[i]
                    i += 1
                else:
                    alist[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                alist[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                alist[k] = right_half[j]
                j += 1
                k += 1
        # print("Merging ", alist)


# Context: is configured with a ConcreteStrategy object
# maintains a reference to a Strategy object
# may define an interface that lets Strategy access its data.
class SortedList:
    _list = None
    _sort_strategy = None

    def __init__(self):
        self._list = []

    def set_sort_strategy(self, sort_strategy):
        self._sort_strategy = sort_strategy

    def add(self, name):
        self._list.append(name)

    def sort(self):
        self._sort_strategy.sort(self._list)

        for name in self._list:
            print(" ", name)



# usage
student_records = SortedList()

student_records.add("Samual")
student_records.add("Jimmy")
student_records.add("Sandra")
student_records.add("Vivek")
student_records.add("Anna")

student_records.set_sort_strategy(QuickSort())
student_records.sort()

student_records.set_sort_strategy(ShellSort())
student_records.sort()

student_records.set_sort_strategy(MergeSort())
student_records.sort()

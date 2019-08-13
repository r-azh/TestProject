class Person:

    def __init__(self, first, last):
        self.first_name = first
        self.last_name = last

    def get_name(self):
        return self.first_name + " " + self.last_name


class Employee(Person):

    def __init__(self, first, last, staff_num):
        Person.__init__(self, first, last)  # We could have used super instead
        self.staff_number = staff_num

    def get_employee(self):
        print(self.get_name(), ", staff_id:", self.staff_number)


class Student(Person):
    def __init__(self, first, last, student_num):
        super().__init__(first, last)       # user super
        self.student_number = student_num

    def get_student(self):
        print(self.get_name(), ", sudent_id:", self.student_number)


x = Person("Marge", "Simpson")
y = Employee("Homer", "Simpson", "1007")
z = Student("Reza", "Rezayi", "90076")

print(x.get_name())
y.get_employee()
z.get_student()

# tach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to
# subclassing for extending functionality.


# Component: defines the interface for objects that can have responsibilities added to them dynamically.
class LibraryItem:
    _num_copies = None

    @property
    def num_copies(self):
        return self._num_copies

    @num_copies.setter
    def num_copies(self, value):
        self._num_copies = value

    def display(self):
        raise NotImplementedError


# ConcreteComponent: defines an object to which additional responsibilities can be attached.
class Book(LibraryItem):
    _author = None
    _title = None

    def __init__(self, author, title, num_copies):
        self._author = author
        self._title = title
        self.num_copies = num_copies

    def display(self):
        print("\nBook ------ ")
        print(" Author: {}".format(self._author))
        print(" Title: {}".format(self._title))
        print(" # Copies: {}".format(self.num_copies))


class Video(LibraryItem):
    _director = None
    _title = None
    _play_time = None

    def __init__(self, director, title, play_time, num_copies):
        self.num_copies = num_copies
        self._director = director
        self._title = title
        self._play_time = play_time

    def display(self):
        print("\nVideo -----")
        print(" Director: {}".format(self._director))
        print(" Title: {}".format(self._title))
        print(" Playtime: {}".format(self._play_time))
        print(" # Copies: {}".format(self.num_copies))


# Decorator: maintains a reference to a Component object and defines an interface that conforms to Component's interface
class Decorator(LibraryItem):
    library_item = None

    def __init__(self, library_item):
        self.library_item = library_item

    def display(self):
        self.library_item.display()


# ConcreteDecorator: adds responsibilities to the component.
class Borrowable(Decorator):
    borrowers = None

    def __init__(self, library_item):
        super().__init__(library_item)
        self.borrowers = []

    def borrow_item(self, name):
        self.borrowers.append(name)
        self.library_item.num_copies -= 1

    def return_item(self, name):
        self.borrowers.remove(name)
        self.library_item.num_copies += 1

    def display(self):
        super().display()

        for borrower in self.borrowers:
            print("borrower: {}".format(borrower))



# usage:
book = Book("Worley", "Inside ASP.NET", 10)
book.display()

video = Video("Spielberg", "Jaws", 23, 92)
video.display()

print("\nMaking video borrowable:")

borrow_video = Borrowable(video)
borrow_video.borrow_item("customer #1")
borrow_video.borrow_item("customer #2")
borrow_video.display()

borrow_video.return_item("customer #1")
borrow_video.display()

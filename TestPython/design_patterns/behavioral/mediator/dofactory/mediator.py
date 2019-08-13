__author__ = 'R.Azh'

# Defines simplified communication between classes
# Define an object that encapsulates how a set of objects interact. Mediator promotes loose coupling by keeping objects
# from referring to each other explicitly, and it lets you vary their interaction independently.
# Mediator pattern facilitates loosely coupled communication between different objects and object types.


# example: one to one chat room

# Mediator: defines an interface for communicating with Colleague objects
class AbstractChatroom:
    def register(self, participant):
        raise NotImplementedError

    def send(self, from_person, to_person, message):
        raise NotImplementedError


# ConcreteMediator: implements cooperative behavior by coordinating Colleague objects
# knows and maintains its colleagues
class Chatroom(AbstractChatroom):
    _participants = None

    def __init__(self):
        self._participants = {}

    def register(self, participant):
        if participant.name not in self._participants:
            self._participants[participant.name] = participant
        participant.chatroom = self

    def send(self, from_person, to_person, message):
        participant = self._participants[to_person]

        if participant:
            participant.receive(from_person, message)


# Colleague classes: each Colleague class knows its Mediator object
# each colleague communicates with its mediator whenever it would have otherwise communicated with another colleague

# AbstractColleague
class Participant:
    _chatroom = None
    _name = None

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def chatroom(self):
        return self._chatroom

    @chatroom.setter
    def chatroom(self, value):
        self._chatroom = value

    def send(self, to_person, message):
        self._chatroom.send(self._name, to_person, message)

    def receive(self, from_person, message):
        print("{} to {}: {}".format(from_person, self._name, message))


# ConcreteColleague
class Beatle(Participant):
    def __init__(self, name):
        super().__init__(name)

    def receive(self, from_person, message):
        print("to a beatle: ")
        super().receive(from_person, message)


# ConcreteColleague
class NonBeatle(Participant):
    def __init__(self, name):
        super().__init__(name)

    def receive(self, from_person, message):
        print("to a non beatle: ")
        super().receive(from_person, message)


# usage
chat_room = Chatroom()

george = Beatle('George')
paul = Beatle('Paul')
ringo = Beatle('Ringo')
john = Beatle('John')
yoko = NonBeatle('Yoko')

chat_room.register(george)
chat_room.register(paul)
chat_room.register(ringo)
chat_room.register(john)
chat_room.register(yoko)

yoko.send("John", "Hi John!")
paul.send("Ringo", "All you need is love")
ringo.send("George", "My sweet Lord")
paul.send("John", "Can't buy me love")
john.send("Yoko", "My sweet love")


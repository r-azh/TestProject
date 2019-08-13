__author__ = 'R.Azh'


class RobotBuildable:
    def go(self):
        raise NotImplementedError


class RobotBuilder:
    def add_start(self):
        raise NotImplementedError

    def add_get_parts(self):
        raise NotImplementedError

    def add_assemble(self):
        raise NotImplementedError

    def add_test(self):
        raise NotImplementedError

    def add_stop(self):
        raise NotImplementedError

    def get_robot(self):
        raise NotImplementedError


class CookieRobotBuildable(RobotBuildable):
    actions = None

    def __init__(self):
        self.actions = []

    def go(self):
        actions_dict = {1: self.start, 2: self.get_parts, 3: self.assemble, 4: self.test, 5: self.stop}
        for act in self.actions:
            actions_dict[act]()

    def start(self):
        print("Starting....")

    def get_parts(self):
        print("Getting flour and sugar....")

    def assemble(self):
        print("Baking a cookie....")

    def test(self):
        print("Crunching a cookie....")

    def stop(self):
        print("Stopping....")

    def load_actions(self, a):
        self.actions = a


class CookieRobotBuilder(RobotBuilder):
    robot = None
    actions = None

    def __init__(self):
        self.actions = []
        self.robot = CookieRobotBuildable()

    def add_start(self):
        self.actions.append(1)

    def add_get_parts(self):
        self.actions.append(2)

    def add_assemble(self):
        self.actions.append(3)

    def add_test(self):
        self.actions.append(4)

    def add_stop(self):
        self.actions.append(5)

    def get_robot(self):
        self.robot.load_actions(self.actions)
        return self.robot


class AutomotiveRobotBuildable(RobotBuildable):
    actions = None

    def __init__(self):
        self.actions = []

    def go(self):
        actions_dict = {1: self.start, 2: self.get_parts, 3: self.assemble, 4: self.test, 5: self.stop}
        for act in self.actions:
            actions_dict[act]()

    def start(self):
        print("Starting....")

    def get_parts(self):
        print("Getting a carburetor....")

    def assemble(self):
        print("Installing the carburetor....")

    def test(self):
        print("Revving the engine....")

    def stop(self):
        print("Stopping....")

    def load_actions(self, a):
        self.actions = a


class AutomotiveRobotBuilder(RobotBuilder):
    robot = None
    actions = None

    def __init__(self):
        self.actions = []
        self.robot = AutomotiveRobotBuildable()

    def add_start(self):
        self.actions.append(1)

    def add_get_parts(self):
        self.actions.append(2)

    def add_assemble(self):
        self.actions.append(3)

    def add_test(self):
        self.actions.append(4)

    def add_stop(self):
        self.actions.append(5)

    def get_robot(self):
        self.robot.load_actions(self.actions)
        return self.robot
    

# TestRobotBuilder
builder = RobotBuilder()
# robot = RobotBuildable()

print("Do you want a cookie robot [c] or an automotive one [a]?")
response = input()

if response == "c":
    builder = CookieRobotBuilder()
elif response == "a":
    builder = AutomotiveRobotBuilder()

builder.add_start()
builder.add_test()
builder.add_assemble()
builder.add_stop()

robot = builder.get_robot()

robot.go()
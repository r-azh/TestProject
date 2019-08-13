__author__ = 'R.Azh'


class Node:
    def __init__(self, value):
        self.left = []
        self.value = value
        self.right = []

    def iterate(self):
        for node in self.left:
            yield from node.iterate()
        yield self.value
        for node in self.right:
            yield from node.iterate()


class NodeRefctored:
    def __init__(self, value):
        self.left = []
        self.value = value
        self.right = []

    def process(self):
        input_value = yield self.value


    def child_iterate(self, nodes):
        for node in nodes:
            yield from node.process()

    def node_iterate(self):
        yield from self.child_iterate(self.left)
        self.process()
        yield from self.child_iterate(self.right)


def main():
    root = Node(0)
    root.left = [Node(i) for i in [1, 2, 3]]
    root.right = [Node(i) for i in [4, 5, 6]]
    # for value in root.iterate():
    #     print(value)
    # or
    it = root.iterate()
    while True:
        try:
            print(it.send(None))
        except StopIteration:
            break
    print('####################################')
    root2 = NodeRefctored(100)
    root2.right = [NodeRefctored(i) for i in [101, 102, 103]]
    root2.left = [NodeRefctored(i) for i in [97, 98, 99]]
    it2 = root2.node_iterate()
    while True:
        try:
            print(it2.send(None))
        except StopIteration:
            break

if __name__ == "__main__":
    main()



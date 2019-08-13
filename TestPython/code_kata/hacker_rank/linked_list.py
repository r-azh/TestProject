__author__ = 'R.Azh'

"""
Detect a cycle in a linked list. Note that the head pointer may be 'None' if the list is empty.

A Node is defined as:

"""

class Node(object):
    def __init__(self, data = None, next_node = None):
        self.data = data
        self.next = next_node


def has_cycle(head):
    if not head:
        return False
    if not head.next:
        return False
    current_node = head
    other_node = head.next.next
    while current_node.next:
        while other_node:
            print(current_node.data, ', ', other_node.data)
            if current_node == other_node:
                return True
            other_node = other_node.next
        current_node = current_node.next
    return False


def has_cycle1(head):
    if not head:
        return False
    current_node = head
    node_addresses = []
    while(current_node.next):
        if current_node.next in node_addresses:
            return True
        else:
            node_addresses.append(current_node)
            current_node = current_node.next
    return False

e = Node('e', None)
d = Node('d', e)
c = Node('c', d)
b = Node('b', c)
a = Node('a', b)
c.next = c

print(has_cycle(a))
from py_dsa.algorithms import *
from py_dsa.data_structures import *

# a = [1, 2, 3, 4.5]
# s = Searching()
# print(s.linear_search(a, 3))

# test_linkedlist = LinkedList()
# test_linkedlist.add_first(10)
# test_linkedlist.add_first(20)
# test_linkedlist.add_first(30)
# test_linkedlist.remove_last()
# test_linkedlist.reverse_list()
# test_linkedlist.print_list()

test_tree = Tree()
test_tree.add(10)
test_tree.add(5)
test_tree.add(30)
print(test_tree.height())
test_tree.invert_tree()
test_tree.print_tree(traversal='postorder')

# test_graph = Graph()
# test_graph.add_edge(0, 1)
# test_graph.add_edge(0, 2)
# test_graph.add_edge(1, 2)
# test_graph.add_edge(2, 0)
# test_graph.add_edge(2, 3)
# test_graph.add_edge(3, 3)
# test_graph.print_graph()
# print(test_graph.breadth_first_search(2))
# print(test_graph.depth_first_search(0))

from linked_binary_tree import LinkedBinaryTree

test_tr = LinkedBinaryTree('a')
print(test_tr)
print("root_val ", test_tr.get_root_val())
print("left_child ", test_tr.get_left_child())
test_tr.insert_left(' b')
print("left_child ", test_tr.get_left_child())
print("left_child().get_root_val ", test_tr.get_left_child().get_root_val())
test_tr.insert_right(' c')
print("right_child ", test_tr.get_right_child())
print("right_child().get_root_val ", test_tr.get_right_child().get_root_val())
test_tr.get_right_child().set_root_val(' hello')
print("right_child().get_root_val", test_tr.get_right_child().get_root_val())

print(test_tr)

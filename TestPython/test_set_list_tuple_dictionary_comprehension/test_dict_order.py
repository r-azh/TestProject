from collections import OrderedDict

__author__ = 'R.Azh'

# dont preserver order
index = {'parent_post_id': 1, 'parent_first_level_comment_id': 1,
                     'container_id': 1, 'creator.person_id': 1}
print(index)

indexes = [(k, v) for k, v in index.items()]
print(indexes, '\n')


# dont preserver order
index = OrderedDict({'parent_post_id': 1, 'parent_first_level_comment_id': 1,
                     'container_id': 1, 'creator.person_id': 1})
print(index)

indexes = [(k, v) for k, v in index.items()]
print(indexes, '\n')

# preserver order
index_list = [('parent_post_id', 1), ('parent_first_level_comment_id', 1),
                                  ('container_id', 1), ('creator.person_id', 1)]

print(index_list)

# preserver order
index = OrderedDict([('parent_post_id', 1), ('parent_first_level_comment_id', 1),
                                  ('container_id', 1), ('creator.person_id', 1)])
print(index)



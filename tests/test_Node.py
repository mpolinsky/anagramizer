# test_Node.py tests the Node class

from tg_proj.TaylorNode import Node

def test_TaylorNode_repr():
    res = Node('alcss', 'genuine ', ['class', 'ass', 'as', 'a'], None)
    print(res)
    assert res.__repr__() == f"""Node({str('alcss')}, {str('genuine ')}, {['class', 'ass', 'as', 'a']})"""

def test_TaylorNode_getters():
    res = Node('alcss', 'genuine ', ['class', 'ass', 'as', 'a'], None)
    attribs = [res.get_name(), res.get_anagram(), res.get_word_pool()]
    assert attribs[0] == 'alcss'
    assert attribs[1] == 'genuine '
    assert attribs[2] == ['class', 'ass', 'as', 'a']

def test_equality():
    a = Node('hello', 'world ', ['hell', 'o', 'el', 'eel'], None)
    assert a == Node('hello', 'world ', ['hell', 'o', 'el', 'eel'], None)




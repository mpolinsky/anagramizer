# test_Node.py tests the Node class
from typing import Generator
from tg_proj.TaylorProblem import TaylorProblem
from tg_proj.TaylorNode import Node

from collections import Counter as Co
import english_words as ew

import pytest

corpus = [i for i in ew.english_words_lower_alpha_set if len(i) > 3]

# is this test no good?  Using the res.shrink_pool in the comparison.
def test_get_start_state():
    res = TaylorProblem(Co('alecguinness'), corpus)
    assert res.get_startState() == Node(Co('alecguinness'), [], res.shrink_pool(Co('alecguinness'), corpus), None)

# test that goalTest returns True when state.pool is empty
def test_TaylorProblem_returns_true_when_pool_is_empty():
    res = TaylorProblem(Co('alecguinness'), [])
    # assert generating children on a state with empty pool returns True
    assert res.goalTest(res.get_startState()) is True

def test_TaylorProblem_returns_false_when_pool_is_not_empty():
    res = TaylorProblem(Co('alecguinness'), ['genuine', 'class'])
    # assert generating children on a state with empty pool returns True
    assert res.goalTest(res.get_startState()) is False

# test that shrink_pool produces a smaller pool than original corpus
def test_shrink_pool_shrinks_pool():
    res = TaylorProblem(Co('alecguinness'), corpus)
    # get length of first state yielded by generateChildren's pool and compare to corpus
    assert len(next(res.generateChildren(res.get_startState())).pool) < len(corpus)

# Check that invalid words are filtered by letter_check
def test_letter_returns_false():
    res = TaylorProblem(Co('alecguinness'), corpus)
    assert res.letter_check(Co('hat'), 'hammond') is False

# Check that a valid word is not filtered out by letter_check
def test_letter_returns_true():
    res = TaylorProblem(Co('alecguinness'), corpus)
    assert res.letter_check(Co('hat'), 'at') is True

# Tests to check that invalid words don't make it through the shrink process
def test_shrink_pool_eliminates_invalid_words():
    res = TaylorProblem(Co('alecguinness'), corpus)
    children = res.generateChildren(res.get_startState())
    state = next(children)
    # Uncomment next two lines if it starts giving you empty pool errors
    while state.pool == []:
         state = next(children)
    pool = state.pool
    name = state.name
    # 'volvo' is in the dev corpus.
    assert 'volvo' not in pool
    assert 'earthmoving' not in pool
    # words are all of correct length
    assert len(max(pool, key=len)) <= sum(name.values())
    # Should have filtered out all words containing letters not in 'alecguinness'
    assert [i for i in pool if 'x' in list(i)] == []
    assert [i for i in pool if 'o' in list(i)] == []
  
# Check that the number of generated children is equal to the number of words in the valid word pool
def test_generate_children_generates_correct_number_of_children():
    res = TaylorProblem(Co('alecguinness'), corpus)
    # get length of reduced word pool
    og_pool_length = len(res.get_startState().pool)
    # create list of all generated children
    parent_node = [i for i in res.generateChildren(res.get_startState())]
    assert len(parent_node) == og_pool_length
    
# Check that the word pool is ordered by length when created
def test_word_pool_ordered_by_length_descending():
    # create problem and get the word pool
    res = TaylorProblem(Co('alecguinness'), corpus)
    state = next(res.generateChildren(res.get_startState()))
    pool = state.pool
    # assert that it is equal to sorting it in descending order by length
    sorted_pool = pool.copy()
    sorted_pool.sort(key=len, reverse=True)
    assert pool == sorted_pool

"""
def test_anagram_is_a_list():
    res = TaylorProblem(Co('alecguinness'), corpus)
    start_state = res.get_startState()
    state = next(res.generateChildren(res.get_startState()))
    assert isinstance(start_state.get_anagram(), list)
    assert isinstance(state.get_anagram(), list)
"""

def test_generateChildren_returns_generator():
    res = TaylorProblem(Co('alecguinness'), corpus)
    state = next(res.generateChildren(res.get_startState()))
    result = res.generateChildren(state)
    assert isinstance(result, Generator)
# Check bad inputs.... 


from typing import Deque, Generator
from tg_proj.Searches import Search
from tg_proj.TaylorProblem import TaylorProblem
import english_words as ew
from collections import Counter as Co
import pytest

corpus = [i for i in ew.english_words_lower_alpha_set if len(i) > 3]

# Check it returns the problem
def test_search_returns_problem():
    res = TaylorProblem(Co('alecguinness'), corpus)
    search = Search(res)
    assert isinstance(search.getProblem(), TaylorProblem)

# check that openList is a deque with a generator on it 
def test_dfs_setup_returns_deque_with_generator():
    search = Search(TaylorProblem(Co('alecguinness'), corpus))
    setup_result = search._DFS_setup()
    assert isinstance(setup_result, Deque)
    assert isinstance(setup_result[0], Generator)

# Check that get_current_state gets the state out of a generator
def test_dfs_get_current_state_good_generator():
    search = Search(TaylorProblem(Co('alecguinness'), corpus))
    results = ['temp_results','for_development']
    closedList = list()
    # add start state to openlist
    openList = search._DFS_setup()
    assert search._get_current_state(openList, closedList, results) == search.getProblem().get_startState()

# check that get_current_state will successfully eject an empty generator 
#      and collect the state from the next one on openList
def test_dfs_get_current_state_empty_generator_with_another_one_in_list():
    results =  ['temp_results','for_development']
    search = Search(TaylorProblem(Co('alecguinness'), corpus))
    openList = Deque()
    openList.append( ( i for i in [] ) )
    openList.append( ( i for i in [search.problem.get_startState()] ) )
    assert search._get_current_state(openList, [], results) == search.getProblem().get_startState()

# chekcs that get_current_state returns the results when 
#   there is only an empty generator left on openList.
def test_dfs_get_current_state_empty_generator_last_on_list():
    results =  ['temp_results','for_development']
    search = Search(TaylorProblem(Co(''), corpus))
    openList = Deque()
    # create an empty generator
    openList.append(( i for i in [] ))
    assert search._get_current_state(openList, [], results, dev=True) == ['temp_results','for_development']


#def test_dfs_appends_to_results_when_pool_and_counter_are_empty():
#    search = Search(TaylorProblem(Co('todjones'), corpus))
#    results = search.DFS()
#    print(*['\n'+i for i in results])
#    assert len(results) == 1

@pytest.mark.xfail(reason='Not implemented')
def test_dfs_finds_dead_ends_and_continues():
    assert 13 == 65

"""
def test_dfs_only_makes_complete_length_anagrams():
    #compare namelength to anagram length for all results.
    og = len('alecguinness')
    search = Search(TaylorProblem(Co('alecguinness'), corpus))
    results = search.DFS()
    assert len(results) == len([i for i in results if len([j for j in i if j != ' ']) == og])
"""

@pytest.mark.xfail()
def test_dfs_correctness():
    # how.
    return 0


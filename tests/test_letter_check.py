from collections import Counter as Co
from tg_proj.letter_check import letter_check, shrink_pool
import pytest

@pytest.fixture()
def pool():
   pool = [
      'hat',
      'at',
      'a',
      'sat',
      'flat',
      'mat',
      'latter',
      'madder',
      'get',
      'but',
      'mop',
      'morph',
      'prom',
      'log',
      'slog',
      'good',
      'top',
      'last',
   ]
   return pool

# letter_check tests

def test_letter_check_rejects_nonmatches():
  assert letter_check(Co('hat'), 'can') == False
 
def test_letter_check_accepts_matches():
  assert letter_check(Co('hat'), 'hat') == True

def test_string_passed_to_letter_check_raises_error():
   assert letter_check('hat', 'hat') raises AttributeError
   
# shrink_pool tests   

def test_shrink_pool_creates_smaller_pools(pool):
  assert len(shrink_pool(Co('hats'), pool)) < len(pool)

def test_shrink_pool_returns_empty_for_no_matches(pool):
  assert shrink_pool(Co('git'), pool) == []



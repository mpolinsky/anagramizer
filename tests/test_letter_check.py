from collections import Counter as Co
from tg_proj.letter_check import letter_check, shrink_pool

def test_letter_check_rejects_nonmatches():
  assert letter_check(Co('hat'), 'can') == False
 
def test_letter_check_accepts_matches():
  assert letter_check(Co('hat'), 'hat') == True

def test_shrink_pool_creates_smaller_pools():
  pool = [
  'hat',
  'at',
  'a',
  'sat',
  'flat',
  'mat',
  'latter',
  'madder'
  ]
  assert len(shrink_pool(Co(hat)))) < len(pool)

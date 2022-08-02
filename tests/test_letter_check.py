from collections import Counter as Co

def test_letter_check():
  from tg_proj.letter_check import letter_check
  assert letter_check(Co('hat'), 'can') == False

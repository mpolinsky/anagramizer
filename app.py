import english_words as ew
from collections import Counter as Co
import streamlit as st

# check for presence and number of letters to eliminate invalid words
def letter_check(self, current_name_counter, candidate_word):
    word_count = Co(candidate_word)
    for letter, count in word_count.items():
        if count > current_name_counter.get(letter, -1):
            return False
    return True

# Keep words that pass the letter_check
def shrink_pool(self, current_name_counter, word_pool):
    newpool = [i for i in word_pool if self.letter_check(current_name_counter, i)]
    newpool.sort(key=len, reverse=True)
    return newpool

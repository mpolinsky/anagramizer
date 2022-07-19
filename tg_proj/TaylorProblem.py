# TaylorProblem.py provides methods and data for the anagramizer.  Named for Simpsons characters Allison Taylor and her father, Prof. Taylor.

from re import A
from tg_proj.TaylorNode import Node
from collections import Counter as Co

class TaylorProblem:
    def __init__(self, name_counter, word_pool):
        self.startState = Node(name_counter, list(), self.shrink_pool(name_counter,word_pool), None)
    
    def get_startState(self):
        return self.startState
    
    def goalTest(self, state):
        if state.pool == []:
            # SUCCESS
           return True
        return False

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

        


    # A generator that yields child nodes 
    def generateChildren(self, state):
        results = list()
        i = 0
        while i < len(state.pool):
            new_anagram = state.anagram.copy()
            print(f'Building new node for anagram: {new_anagram}')
            new_anagram.append(state.pool[i])
            print(f'New word to add: {state.pool[i]}')

            print(f'New anagram: {new_anagram}')
            new_counter = state.name - Co(''.join(new_anagram))

            new_pool = self.shrink_pool(new_counter, state.pool)
            print(f'new pool size: {len(new_pool)}')
            i += 1
            # Create and add node with new name, new pool, and new word for anagram, plus parent ref
            yield Node(new_counter, new_anagram, new_pool, self)
   
          

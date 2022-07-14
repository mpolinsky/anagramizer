import english_words as ew
from collections import Counter as Co
import streamlit as st

WORDLIMIT = 4

# check for presence and number of letters to eliminate invalid words
def letter_check(current_name_counter, candidate_word):
    word_count = Co(candidate_word)
    for letter, count in word_count.items():
        if count > current_name_counter.get(letter, -1):
            return False
    return True

# Keep words that pass the letter_check
def shrink_pool(current_name_counter, word_pool):
    newpool = [i for i in word_pool if letter_check(current_name_counter, i)]
    newpool.sort(key=len, reverse=True)
    return newpool

def run(counter, wordpool):
    # shrink pool
    new_pool = shrink_pool(counter, wordpool)
    # choose a word and collect word
    with st.form(key='columns_in_form'):
        col1, col2 = st.columns(2)
        word = col1.selectbox(f'Make a Selection', new_pool)
        submitted = col1.form_submit_button('Select')
        if submitted:
            col1.write("SUBMITTED")
    
    # adjust counter
    new_counter = counter - Co(word)
    return word, counter, wordpool

def main():
    results = list()
    corpus = [i for i in ew.english_words_lower_alpha_set if len(i) > WORDLIMIT]
    name = st.text_input("Enter name: ")
    name = name.lowercase()
    name = name.replace(' ','')
    counter = Co(name)
    pool = 1
    while counter != {} and pool != []:
        word, counter, pool = run(counter, pool)
        results.append(word)
    st.subheader(' '.join(results))
        
main()

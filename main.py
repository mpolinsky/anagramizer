import english_words as ew
from collections import Counter as Co
import streamlit as st
from datetime import datetime as dt


st.cache()
def get_name():
    name = st.text_input("Enter name: ").lower().strip().replace(' ','')
    return name, Co(name)

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

def reduce_round():
    # declare streamlit state variables 
    WORDLIMIT = 4
    name, counter = get_name()
    word_pool = shrink_pool(
        counter,
        [i for i in ew.english_words_lower_alpha_set if len(i) > 4]
        )
    return name, counter, word_pool

st.header("Are we here?")

def main_loop():
    st.subheader("Session State")
    st.write(list(st.session_state.keys()))
    name, counter, word_pool = reduce_round()
    st.subheader("Session State")
    st.write(list(st.session_state.keys()))
    next_word = st.selectbox(label="Choose next word", options=word_pool, key=str(dt.now()))
    st.write(next_word)
    st.subheader("End")

while True:    
    main_loop()



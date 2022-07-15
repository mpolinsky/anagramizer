import english_words as ew
from collections import Counter as Co
import streamlit as st
from datetime import datetime as dt
import time

st.cache(allow_output_mutation=True)
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


st.subheader("Session State")
st.write(list(st.session_state.keys()))

# Generate initial values name, the first name counter, and the initially reduced corpus
name, counter = get_name()
word_pool = shrink_pool(counter, [i for i in ew.english_words_lower_alpha_set if len(i) > 4])
    
# we want to tdisplay the pool tot he user for now in a selectbox list 
next_word = st.selectbox(label="Choose next word", options=word_pool, key=str(dt.now()))
# now the user has selected and stored a word.  We need to repeat this process until the pool returns empty.
while word_pool != []:
    st.write(next_word)
    time.sleep(1)
    counter = counter - Co(next_word)
    word_pool = shrink_pool(counter, word_pool)
    next_word = st.selectbox(label="Choose next word", options=word_pool, key=str(dt.now()))
    
st.subheader("Pool exhausted")

st.subheader("Session State")
st.write(list(st.session_state.keys()))

st.subheader("End")



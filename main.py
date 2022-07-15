import english_words as ew
from collections import Counter as Co
import streamlit as st
from datetime import datetime as dt
import time




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

@st.cache(suppress_st_warning=True)
def setup():
    name = st.text_input("Enter name: ").lower().strip().replace(' ','')
    pool = shrink_pool(Co(name), [i for i in ew.english_words_lower_alpha_set if len(i) > 4])
    st.session_state['results'] = list()
    return name, pool


st.subheader("Session State")
st.write(list(st.session_state.keys()))

def main(name_counter, word_pool):
    word_pool = shrink_pool(name_counter, word_pool)
    word_choice = st.selectbox(label="Choose", options=word_pool, key=str(dt.now()))
    return word_choice, name_counter - Co(word_choice), word_pool
                 
# Generate initial values name, the first name counter, and the initially reduced corpus
name, word_pool = setup()

while word_pool != []:
    word_choice, new_Counter, word_pool = main(Co(name), pool)
    st.session_state['results'].append(word_choice)


st.header(list(st.session_state['results']))
st.subheader("End")



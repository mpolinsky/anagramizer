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
    st.write(f"current counter: {current_name_counter}")
    st.write(f"wordpool len: {len(word_pool)}")
    newpool = [i for i in word_pool if letter_check(current_name_counter, i)]
    newpool.sort(key=len, reverse=True)
    st.write(f"in shrink pool: returned pool size is {len(newpool)}")
    return newpool

st.title('You can do it!')

if 'word_pool' not in st.session_state:
    st.session_state.word_pool = ['happy', 'delighted', 'glad']#[i for i in ew.english_words_lower_alpha_set if len(i) > 3]

if 'count' not in st.session_state:
    st.session_state.count = 0

increment = st.button('Increment')
if increment:
    st.session_state.count += 1

st.write('Count = ', st.session_state.count)
    
option = st.selectbox(
 'Select a word',
 st.session_state.word_pool)

st.write('You selected:', option)

title = st.text_input('Movie title', 'Life of Brian')
st.write('The current movie title is', title)
st.session_state.word_pool.append(title)

    
    
    

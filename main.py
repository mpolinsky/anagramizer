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

def reset_values():
    # set new counter
    st.session_state.counter = st.session_state.counter - Co(st.session_state.choice)
    st.session_state.results.append(st.session_state.choice)
    st.session_state.word_pool = shrink_pool(st.session_state.counter, st.session_state.word_pool)


st.title('You can do it!')

if 'results' not in st.session_state:
    st.session_state['results'] = []
    st.session_state['name'] = st.text_input("Enter name: ").lower().replace(' ','')
    st.session_state['counter'] = Co(st.session_state.name)
    st.session_state]'word_pool'] = shrink_pool(st.session_state.counter, [i for i in ew.english_words_lower_alpha_set if len(i) > 4])

st.subheader(st.session_state.results) 
st.subheader(st.session_state.name)
st.subheader(st.session_state.counter) 
st.subheader(st.session_state.word_pool) 

st.header(f"Session name is: {st.session_state.name}")
if st.session_state.results != []:
    st.header(f"Session name is: {' '.join(st.session_state.results)}")
else:
    st.header(f"No anagram yet.")
st.subheader(f"Word pool length is {len(st.session_state.word_pool)}")
st.session_state.choice = st.selectbox(label="Select word", options=st.session_state.word_pool, key=dt.now())
#submit = st.button('Next word', on_click=reset_values)
st.session_state.counter = st.session_state.counter - Co(st.session_state.choice)

st.session_state.results.append(st.session_state.choice)

#if submit:
st.write(f'Results = {st.session_state.results}')
    
    
    
    

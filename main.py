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

if 'results' not in st.session_state:
    st.write("Doing setup...")
    st.session_state['results'] = []
    name = st.text_input("Enter name: ").lower().replace(' ','')
    st.header(f"Name: {name}")
    st.session_state['name'] = name
    #st.session_state['counter'] = Co(name)
    #st.session_state['word_pool'] = shrink_pool(st.session_state.counter, [i for i in ew.english_words_lower_alpha_set if len(i) > 4])
    st.session_state.count = 0
    
#st.subheader(st.session_state['counter']) 
#st.subheader(st.session_state['word_pool']) 

#st.header(f"Session name is: {st.session_state['name']}")
#if st.session_state.results != []:
    #st.header(f"Session anagram is: {' '.join(st.session_state['results'])}")
#else:
    #st.header(f"No anagram yet.")
st.subheader(f"Word pool length is {len(st.session_state['word_pool'])}")
c = st.selectbox(label="Select word", options=st.session_state.word_pool, key=dt.now())
st.session_state.choice = c
st.write(f"Choice is: {c}")
st.write(f"Choice is {st.session_state.choice}")
st.session_state.counter = st.session_state.counter - Co(st.session_state.choice)

st.session_state.results.append(st.session_state.choice)
#submit = st.button('Next word', key=dt.now())
#if submit:
#    st.session_state.count += 1
#st.header(f"Count: {st.session_state.count}")
#if submit:
st.write(f'Results = {st.session_state.results}')

st.title('Counter Example')
    

increment = st.button('Increment')
if increment:
    st.session_state.count += 1

st.write('Count = ', st.session_state.count)

for i in list(st.session_state.items()):
    st.write(i)
    
    
    

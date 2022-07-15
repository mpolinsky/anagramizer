import english_words as ew
from collections import Counter as Co
import streamlit as st
from datetime import datetime


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

st.header("Are we here?")
# declare streamlit state variables 
WORDLIMIT = 4
name, counter = get_name()
word_pool = shrink_pool(
    counter,
    [i for i in ew.english_words_lower_alpha_set if len(i) > 4]
    )

st.subheader("Session State")
st.write(st.session_state.keys())







"""
def run(counter, wordpool):
    # shrink pool
    new_pool = shrink_pool(counter, wordpool)
    with st.form(clear_on_submit=True, key=f'{datetime.now()}'):
        # choose a word and collect word
        word = st.selectbox(f'Make a Selection', new_pool)
        submitted = st.form_submit_button('Submit')
        if submitted:    
            # adjust counter
            new_counter = counter - Co(word)
        return word, counter, new_pool


def main():
    results = list()
    pool = [i for i in ew.english_words_lower_alpha_set if len(i) > WORDLIMIT]
    name = st.text_input("Enter name: ").lower()
    name = name.replace(' ','')
    counter = Co(name)
    word, counter, pool = run(counter, pool)
    results.append(word)
    if pool == []:
        st.subheader(' '.join(results))
        
main()
"""

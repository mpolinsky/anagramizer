import streamlit as st
import english_words as ew
from datetime import datetime as dt
from collections import Counter as Co
from random import randint as rand



# check for presence and number of letters to eliminate invalid words
def letter_check(current_name_counter, candidate_word):
    word_count = Co(candidate_word)
    for letter, count in word_count.items():
        if count > current_name_counter.get(letter, -1):
            return False
    return True


# Keep words that pass the letter_check
def shrink_pool(current_name_counter, word_pool):
    newpool = [i for i in word_pool if letter_check(current_name_counter, i) and i is not None]
    newpool.sort(key=len, reverse=True)
    return newpool


@st.cache(allow_output_mutation=True)
def reset_counter(a_name):
    st.session_state.counter1 = Co(st.session_state.name)

st.title("main")

# Streamlit runs from top to bottom on every iteraction so we check the state
if 'word_pool' not in st.session_state:
    st.session_state.word_pool = [i for i in ew.english_words_lower_alpha_set if len(i) > 3]

if 'res' not in st.session_state:
    st.session_state.res = list()

if 'choice' not in st.session_state:
    st.session_state.choice = 'init'

if 'count' not in st.session_state:
    st.session_state.count = 0

if 'name' not in st.session_state or st.session_state.name == "":
    st.session_state.name = st.text_input("Enter name").lower().replace(' ','')

if 'reset' not in st.session_state:
	st.session_state.reset = False
	
if 'random' not in st.session_state:
	st.session_state.random = rand(1,100000)
		
reset_counter(st.session_state.name, st.session_state.random)


if st.session_state.name != "":
	st.session_state.word_pool = shrink_pool(st.session_state.counter1, st.session_state.word_pool)
	st.session_state.word_pool.insert(0, None)
	st.subheader("Select a word and click the select button to move on to the next word!")
	selection = st.selectbox(
	'Select:',
	options = st.session_state.word_pool,
	)
	st.session_state.choice = selection
	st.session_state.res.append(st.session_state.choice)
	st.session_state.counter1 -= Co(st.session_state.res[st.session_state.count])
	
	if [i for i in st.session_state.word_pool if i is not None] == []:
		if st.session_state.counter1 == {}:
			st.subheader(f"Congrats you found a true anagram for {st.session_state.name}!")
			st.header(' '.join([i for i in st.session_state.res if i is not None]))
		else:
			st.subheader(f"Oh, it turns out that doesn't make a complete anagram (as far as we can tell).")
			st.subheader(f"Here is your partial anagram: {' '.join([i for i in st.session_state.res if i is not None])}")
			st.subheader(f"And your leftover letters are: {[ str(i)*st.session_state.counter1[i] for i in st.session_state.counter1 ]}")
		st.subheader("Thanks for playing!  Hit the button below to reset and try another one!!!")
		st.session_state.reset = True
	if not st.session_state.reset:
		st.session_state.count += 1
		st.button("Select")
	else:
		st.subheader("Click reset twice to start again!")
		if st.button("Reset"):
			st.session_state.clear()
			
		else:
			st.write("That's all!")
else:
	del st.session_state.word_pool

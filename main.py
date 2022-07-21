import streamlit as st
import english_words as ew
from datetime import datetime as dt
from collections import Counter as Co




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
    #st.session_state.word_pool = newpool
    return newpool


@st.cache(allow_output_mutation=True)
def reset_counter(a_name):
    st.session_state.counter1 = Co(st.session_state.name)

#@st.cache(allow_output_mutation=True)
def turnabout(oparg):
    st.header("CLICK")
    st.write(f"session_state.choice {st.session_state.choice}")
    st.write(f"Choice passed to callback: {oparg}")
    st.session_state.choice = oparg
    st.session_state.res.append(st.session_state.choice)
    st.header(f"st.session_state.choice is now: {st.session_state.choice}")
    st.session_state.counter1 -= Co(st.session_state.res[st.session_state.count])
    st.subheader(st.session_state.counter1)

st.title("implement selectbox control")


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
    st.session_state.name = st.text_input("Enter name")
		
reset_counter(st.session_state.name)


#if st.session_state.count > 3:
#    st.session_state.res = st.session_state.res[:-1]
if st.session_state.name != "":
	st.write('Count = ', st.session_state.count)
	st.session_state.word_pool = shrink_pool(st.session_state.counter1, st.session_state.word_pool)
	st.session_state.word_pool.insert(0, None)
	#with st.form(key="wordform"):
	selection = st.selectbox(
	'Select:',
	options = st.session_state.word_pool,
	)
	st.session_state.choice = selection
	st.session_state.res.append(st.session_state.choice)
	st.header(f"st.session_state.choice is now: {st.session_state.choice}")
	st.session_state.counter1 -= Co(st.session_state.res[st.session_state.count])
	st.subheader(st.session_state.counter1)
		#submit = st.form_submit_button("Submit", )#on_click=turnabout, args=(selection,))
	#if submit:
		#st.session_state.choice = selection
	st.subheader(st.session_state.counter1)
	if st.session_state.counter1 == {} and st.session_state.res[0] is not None:
		st.subheader(' '.join([ i for i in st.session_state.res if i is not None ]))
	st.session_state.count += 1
	st.button("Next")
else:
    del st.session_state.word_pool

st.write(st.session_state)


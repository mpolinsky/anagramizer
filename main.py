import streamlit as st
import english_words as ew
import wikipedia as wk
from datetime import datetime as dt
from collections import Counter as Co
from random import randint as rand
import requests
import json


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


def get_definition(word):
    api_key= st.secrets['dk']
    URL = "https://dictionaryapi.com/api/v3/references/collegiate/json/"+word+"?key="+api_key
    PARAMS = {'word': word,'key': api_key}
    r = requests.get(url = URL, params = PARAMS)
    return '; '.join(r.json()[0]['shortdef'])


# Retrieves the beginning of article summaries from wikipedia
def retrieve_data(items):
	for index, item in enumerate(items):
		st.subheader(f"{items[index]}")
		try:
			st.write(get_definition(item)+" [(Merriam-Webster)](https://www.merriam-webster.com/dictionary/"+item+")")
		except TypeError:
			st.write(f"This may not be a word, becuase it's not found in Merriam-Webster's Collegiate Dictionary")
		try:
			st.write(wk.summary(items[index], auto_suggest=False).split('\n')[0][:360]+'...[(Wikipedia)](http://www.wikipedia.org/wiki/'+item+')')
		except wk.DisambiguationError:
			st.write(f" ")
			st.write(wk.summary(wk.search(items[index]), auto_suggest=False).split('\n')[0][:360]+'...[(Wikipedia)](http://www.wikipedia.org/wiki/'+item+')')
		
@st.experimental_memo
def reset_counter(a_name):
    st.session_state.counter1 = Co(st.session_state.name)
    st.session_state.part1 = True

st.title("fix-api-bad-response")

# This prevents an error when the user refreshes instead of resetting via the reset button.  
##  Still leaves them at a false success screen with blank data.   					****** Bug to fix here
if 'word_pool' in st.session_state and st.session_state.word_pool == [] and st.session_state.name == "":
	st.session_state.clear()
	reset_counter.clear()

# Streamlit runs from top to bottom on every iteraction so we check the state
if 'word_pool' not in st.session_state:
    st.session_state.word_pool = [i for i in ew.english_words_lower_alpha_set if len(i) > 2] + ['a', 'on']

if 'res' not in st.session_state:
    st.session_state.res = list()

if 'choice' not in st.session_state:
    st.session_state.choice = 'init'

if 'count' not in st.session_state:
    st.session_state.count = 0

if 'name' not in st.session_state or st.session_state.name == "":
    st.session_state.og_name = st.text_input("Enter name")
    st.session_state.name = st.session_state.og_name.lower().replace(' ','')
	
if 'user_anagram' not in st.session_state:
	st.session_state.user_anagram = False
	st.session_state.anagram = None

if 'part1' not in st.session_state:
	st.session_state.part1 = False
	st.session_state.part2 = False

if 'success' not in st.session_state:
	st.session_state.success = False
	
if 'summaries' not in st.session_state:
	st.session_state.summaries = list()
	
if 'reset' not in st.session_state:
	st.session_state.reset = False

		
reset_counter(st.session_state.name)


if st.session_state.name != "":	
	## Part 1
	if st.session_state.part1:
		st.header(f"  ")
		st.header(f"  ")
		st.header(f"  ")
		st.header(f"Current anagram:  \n{' '.join([i for i in st.session_state.res if i is not None])}")
		st.header(f"Letters remaining:  \n  \t{''.join([ str(i)*st.session_state.counter1[i] for i in st.session_state.counter1 ]).replace('',' ')}")
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
			st.session_state.part1 = False
			st.experimental_rerun()
	else:
		st.session_state.part2 = True
	## Part 2
	if st.session_state.part2:
		st.header(f"  ")
		st.header(f"  ")
		st.header(f"  ")
		st.header(f"  ")
		if st.session_state.counter1 == {}:
			st.subheader(f"Congrats you found a true anagram for {st.session_state.og_name}!")
			colM, colN, colO = st.columns([1,3,.1])
			with colN:
				st.header(' '.join([i for i in st.session_state.res if i is not None]).capitalize())
				st.write(f"Copy and past:  \n  \t{' '.join([i for i in st.session_state.res if i is not None])}")
			st.session_state.success = True
		else:
			st.subheader(f"Oh, it turns out that doesn't make a complete anagram...")
			colX, colY = st.columns([1.5,2.5])
			with colY:
				st.subheader(f"...as far as we can tell")
			st.header(f"  ")
			st.subheader(f"Here is your partial anagram:  \n  \t{' '.join([i for i in st.session_state.res if i is not None])}")
			st.subheader(f"And your leftover letters are:  \n  \t{ ''.join([ str(i)*st.session_state.counter1[i] for i in st.session_state.counter1 ]).replace('',' ') }")
			st.subheader(f"  ")
			colA, colB, colC = st.columns([.25, 3.5, .25])
			with colB:
				st.subheader(f"Click here if you see an anagram we missed!")
			col1, col2, col3 = st.columns(3)
			with col2:
				button_press = st.button("Oops!")
			if button_press:
				st.session_state.user_anagram = True
			st.subheader(f"  ")
			# If user wants to enter an anagram:
			if st.session_state.user_anagram:
				# Get user suggestion for anagram
				st.session_state.anagram = st.text_input("If you see an anagram we've missed type it here!", value=None)
				# Celebrate and display success message
				if Co(st.session_state.anagram.lower().replace(' ','')) == Co(st.session_state.name):
					st.subheader(f"You were right! {st.session_state.anagram} is an anagram for {st.session_state.og_name}")
					st.subheader(f"  ")
					st.session_state.success = True
					st.balloons()
				elif st.session_state.anagram != 'None':
					st.subheader("That actually is not a complete anagram, so sorry.")
					
		st.session_state.reset = True
	if not st.session_state.reset:
		st.session_state.count += 1
		st.button("Select")             # THIS IS THE PHANTOM BUTTON ITS HERE ITS HERE!!!!
	else:	
		# Display dropdown
		if st.session_state.success:
			with st.expander("What do these words mean??"):
				st.session_state.summaries = retrieve_data(st.session_state.anagram.split(' ')) if st.session_state.user_anagram else retrieve_data([i for i in st.session_state.res if i is not None])
				st.subheader(f"  ")
				
		colD, colE, colF = st.columns([.95, 2.5, .55])
		with colE:
			st.subheader("Thanks for playing")
		colA, colB, colC = st.columns([.25, 3.5, .25])
		with colB:
			st.subheader("Click twice on the reset button to try another!")
		col1, col2, col3 = st.columns(3)
		with col2:
			big_reset = st.button("Reset")
		if big_reset:
			st.session_state.clear()
			reset_counter.clear()
else:
	del st.session_state.word_pool

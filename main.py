import streamlit as st
import english_words as ew
import wikipedia as wk
from datetime import datetime as dt
from collections import Counter as Co
from random import choice, randint as rand
import requests
import json
import string

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(page_title="Anagramizer", page_icon=':random:', layout="centered", initial_sidebar_state="auto", menu_items=None)


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
			st.write(f"""{get_definition(item)} [(Merriam-Webster)](https://www.merriam-webster.com/dictionary/+{item}+)""")
		except TypeError:
			st.write(f"""This may not be a word, becuase it's not found in Merriam-Webster's Collegiate Dictionary""")
		try:
			st.write(wk.summary(items[index], auto_suggest=False).split('\n')[0][:360]+"... [(Wikipedia)](https://www.wikipedia.org/wiki/"+item+")")
		except wk.exceptions.DisambiguationError:
			st.write(f" ")
			try:
				sum_text = wk.summary(wk.search(items[index])[0], auto_suggest=False)
				sum_text = sum_text.split('\n')[0][:360] if isinstance(sum_text, str) else sum_text[0].split('\n')[0][:360]
			except wk.exceptions.DisambiguationError as de:
				sum_text = choice(de.options)
			finally:
				st.write(f"""{sum_text}... [(Wikipedia)](https://www.wikipedia.org/wiki/"+item+")""")

			#st.write(   wk.summary(wk.search(items[index]), auto_suggest=False)  .split('\n')[0][:360]+'...[(Wikipedia)](http://www.wikipedia.org/wiki/'+item+')')
		except wk.exceptions.PageError:
			st.write("...This doesn't seem to be returning any results from Wikipedia.  It's very possibly not a thing.")
			
@st.experimental_memo
def reset_counter(a_name):
    st.session_state.counter1 = Co(st.session_state.name)
    st.session_state.part1 = True

st.title("sharability-twitter")

st.info("Enter a name and hit enter to start building an anagram word-by-word... But not all combinations lead to complete anagrams!")

# This prevents an error when the user refreshes instead of resetting via the reset button.  
##  Still leaves them at a false success screen with blank data.   					****** Bug to fix here
if 'word_pool' in st.session_state and st.session_state.word_pool == [] and st.session_state.name == "":
	st.session_state.clear()
	reset_counter.clear()

# Streamlit runs from top to bottom on every iteraction so we check the state
if 'word_pool' not in st.session_state:
    st.session_state.word_pool = [i for i in ew.english_words_lower_alpha_set if len(i) > 2] + ['a', 'on', 'in', 'at', 'to', 'too', 'he', 'she', 'as', 'ad']

if 'res' not in st.session_state:
    st.session_state.res = list()


if 'choice' not in st.session_state:
    st.session_state.choice = 'init'

if 'name' not in st.session_state or st.session_state.name == "":
    st.session_state.og_name = st.text_input("Enter name")
    # If there are numbers or symbols don't save them in the og_name. Assume its a mistake.  Can change this if the corpus allows.
    if [i for i in st.session_state.og_name if i in string.punctuation + string.digits ] != []:
        st.session_state.og_name = ''.join([i for i in st.session_state.og_name if i not in string.punctuation + string.digits ])
    st.session_state.name = ''.join([i for i in st.session_state.og_name.lower() if i not in string.whitespace])

if 'user_anagram' not in st.session_state:
	st.session_state.user_anagram = False
	st.session_state.anagram = None

if 'part1' not in st.session_state:
	st.session_state.part1 = False
	st.session_state.part2 = False

if 'success' not in st.session_state:
	st.session_state.success = False
	
if 'oops' not in st.session_state:
	st.session_state.oops = False
	
if 'summaries' not in st.session_state:
	st.session_state.summaries = list()

if 'showfail' not in st.session_state:
	st.session_state.showfail = True
	
if 'jump_to_end' not in st.session_state:
	st.session_state.jump_to_end = False

if 'failend' not in st.session_state:
	st.session_state.failend = False

if 'balloons' not in st.session_state:
	st.session_state.balloons = 0
	
if 'info_render' not in st.session_state:
	st.session_state.info_render = 0
	
if 'disable_manual_entry_fail_warning' not in st.session_state:
	st.session_state.disable_manual_entry_fail_warning = False
	
if 'reset' not in st.session_state:
	st.session_state.reset = False

		
reset_counter(st.session_state.name)


if st.session_state.name != "":	
	## Part 1
	if st.session_state.part1:
		st.header(f"  ")
		st.header(f"  ")
		st.header(f"  ")
		st.subheader(f"""Current anagram:  \n \t{' '.join([i for i in st.session_state.res if i is not None])}""")
		st.subheader(f"""Letters remaining:  \n  \t{''.join([ str(i)*st.session_state.counter1[i] for i in st.session_state.counter1 ]).replace('',' ')}""")
		
		st.session_state.word_pool = shrink_pool(st.session_state.counter1, st.session_state.word_pool)
		if [i for i in st.session_state.word_pool if i != "Select a word!"] == []:
			st.session_state.part1 = False
			st.experimental_rerun()
		st.session_state.word_pool.insert(0, "Select a word!")
		
		st.write("Select a word and click the select button to move on to the next word.  The menu will automatically change.")
		
		with st.form(key="wordform", clear_on_submit=True):
			selection = st.selectbox(
			'Choose the next word!',
			options = st.session_state.word_pool,
			)
			##
			## you'll have to do all the input handling here to...make it its own func...
			manual_entry = st.text_input("Or enter a word here!")
			if manual_entry and manual_entry != "Select a word!" and manual_entry is not None:
				if letter_check(st.session_state.counter1, manual_entry):
					selection = manual_entry
				if not letter_check(st.session_state.counter1, manual_entry):
					st.warning("Remember you can only use the remaining letters!")
					selection = "Select a word!"
			form_submit = st.form_submit_button("Select")
			if form_submit:	
				st.session_state.choice = selection
				if st.session_state.choice == "Select a word!":
					st.session_state.res.append(None)
				else:
					st.session_state.res.append(st.session_state.choice)
				st.session_state.counter1 -= Co(st.session_state.res[-1])
				st.subheader(f"""Choice: {st.session_state.choice}""")
				st.experimental_rerun()
		# Resets from any stage of building
		if st.button("Start over"):
			st.subheader("Starting fresh!")
			st.session_state.clear()
			reset_counter.clear()
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
			st.subheader(f"Congratulations you found a true anagram for {st.session_state.og_name}!")
			colM, colN, colO = st.columns([1.5,3,.1])
			with colN:
				st.header(' '.join([i for i in st.session_state.res if i is not None]).capitalize())
			#st.subheader(f"""Copyable:  \t{' '.join([i for i in st.session_state.res if i != "Select a word!"])}""")
			st.code(f"""{' '.join([i for i in st.session_state.res if i is not None])}""")
			st.session_state.success = True
		else: #elif not st.session_state.oops:
			if st.session_state.showfail:
				st.subheader(f"Oh, it turns out that doesn't make a complete anagram...")
				colX, colY = st.columns([1.5,2.5])
				with colY:
					st.subheader(f"...as far as we can tell")
				#st.session_state.showfail = False
			st.header(f"  ")
			st.subheader(f"""Here is your partial anagram:  \n  \t{' '.join([i for i in st.session_state.res if i is not None])}""")
			st.subheader(f"""And your leftover letters are:  \n  \t{ ''.join([ str(i)*st.session_state.counter1[i] for i in st.session_state.counter1 ]).replace('',' ') }""")
			st.subheader(f"  ")
			if st.session_state.showfail:
				colA, colB, colC = st.columns([.25, 3.5, .25])
				with colB:
					st.subheader(f"Click 'Oops!' if you see an anagram we missed!")
				colM, colN, colO = st.columns(3)
				with colN:
					button_press = st.button("Oops!")
					if button_press:
						st.session_state.user_anagram = True   ####### This is where the oops is pressed.  
						st.session_state.oops = True
						st.session_state.showfail = False
			st.subheader(f"  ")
		
			# If user wants to enter an anagram:
			if st.session_state.user_anagram:
				# Get user suggestion for anagram
				st.session_state.anagram = st.text_input("If you see an anagram we've missed type it here!", value=None)
				# Celebrate and display success message
				if Co(st.session_state.anagram.lower().replace(' ','')) == Co(st.session_state.name):
					st.subheader(f"You were right! {st.session_state.anagram} is an anagram for {st.session_state.og_name}")
					st.subheader(f"  ")
					st.code(f"{st.session_state.anagram}")
					st.session_state.success = True
					if st.session_state.balloons == 0:
						st.balloons()
						st.session_state.balloons += 1
				elif st.session_state.anagram != 'None':
					st.subheader("That actually is not a complete anagram, so sorry.")		

		st.session_state.reset = True
		
	if st.session_state.reset:
		# Display dropdown
		if st.session_state.success or st.session_state.jump_to_end: 
			if st.session_state.info_render < 1 and not st.session_state.jump_to_end:
				with st.expander("What do these words mean??"):
					st.session_state.summaries = retrieve_data(st.session_state.anagram.split(' ')) if st.session_state.user_anagram else retrieve_data([i for i in st.session_state.res if i is not None])
					st.subheader(f"  ")
					st.write("Note: If a Wikipedia search returns many results, the summary dislpayed here could be any of them.  Use the link to see the list!")	
					st.session_state.info_render += 1
			tweet_data = st.session_state.anagram if st.session_state.user_anagram else ' '.join([i for i in st.session_state.res if i != "Select a word!"])
			share_link = f"""https://twitter.com/share?text={tweet_data}"""
			components.html("""<script src="https://platform.twitter.com/widgets.js" charset="utf-8"></script><a href="""+share_link+""" class="twitter-share-button" data-show-count="false">Tweet</a>""")
		
		colA, colB, colC = st.columns([.25, 3.5, .25])
		with colB:
			st.subheader("Click the reset button to try another!")
		col1, col2, col3 = st.columns(3)
		with col2:
			big_reset = st.button("Reset")
		if big_reset:
			st.session_state.clear()
			reset_counter.clear()
			st.experimental_rerun()

else:
	del st.session_state.word_pool

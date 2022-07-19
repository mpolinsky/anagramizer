# main.py is for test running the taylor game
from typing import Set
from tg_proj.Searches import Search
from tg_proj.TaylorNode import Node
from tg_proj.TaylorProblem import TaylorProblem as TP
import english_words as ew
from collections import Counter as Co
import streamlit as st
from datetime import datetime as dt

def main():
    corpus = set([i for i in ew.english_words_lower_alpha_set if len(i) > 3])

    #corpus = ['class', 'genuine','g', 'in', 'lucas', 'salamander', 'art', 'ace', 'guess', 'lace', 'green', 'gables', 'guinness', 'acres', 'grows', 'hours', 'subliminal', 'seen']


    #corpus += ['a','I', 'in', 'or', 'me', 'the', 'my', 'and']
    name = input('enter lowercased name with no spaces')
    search = Search(TP(Co(name), corpus))
    results = search.DFS()
    """
    if isinstance(results[0], Set):
        results = [' '.join(list(i)) for i in results]
    """
    st.session_state.ogname=name

    clean = []
    for i in results:
        if set(i.split(' ')) not in clean:
            clean.append(set(i.split(' ')))
    print(f'length results: {len(results)}\nlength clean: {len(clean)}')

    print(f'{len(results)} anagrams were generated.  Would you like to view them?')
    
  
    #a_dict = {i:len(i.split(' ')) for i in results}
    #print(f"Counter: {Co(a_dict)}")

    if 'anagram' not in st.session_state:
        st.session_state['anagram'] = ''

    choice =int(input('Enter 1 for yes and 0 for no:'))
    st.header(f"Anagrams for {name}:")
    if choice == 1:
        with st.container():
            choices = st.selectbox('Select a word',options=[i.split(' ')[0] for i in results], key=dt.now())
            st.session_state.anagram += choices
         
        st.subheader(st.session_state.anagram)
                
            #for i in results:
                #st.write(i)
            
        #print(*['\n'+i for i in results])
    else:
        with open('anagrams.txt','a+') as outf:
            outf.write(name+'\n')
            for i in results:
                outf.write(i+'\n')
            outf.write('======================\n\n')

            
            
if __name__ == '__main__':
    main()
    print(f'All done.')

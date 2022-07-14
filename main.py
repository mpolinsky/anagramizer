# main.py is for test running the taylor game
from typing import Set
from tg_proj.Searches import Search
from tg_proj.TaylorNode import Node
from tg_proj.TaylorProblem import TaylorProblem as TP
import english_words as ew
from collections import Counter as Co

def main():
    corpus = [i for i in ew.english_words_lower_alpha_set if len(i) > 3]
    name = input('enter lowercased name with no spaces')
    search = Search(TP(Co(name), corpus))
    results = search.DFS()
    """
    if isinstance(results[0], Set):
        results = [' '.join(list(i)) for i in results]
    """
    print(f'{len(results)} anagrams were generated.  Would you like to view them?')
    
    choice =int(input('Enter 1 for yes and 0 for no:'))
    
    
    if choice == 1:
        print(*['\n'+i for i in results])
    else:
        with open('anagrams.txt','a+') as outf:
            outf.write(name+'\n')
            for i in results:
                outf.write(i+'\n')
            outf.write('======================\n\n')


if __name__ == '__main__':
    main()
    print(f'All done.')

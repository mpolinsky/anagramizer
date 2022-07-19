# Searches.py contains the Searches class, 
# which contains the DFS and BFS methods.
from asyncio import SubprocessTransport
from collections import deque as dq
from re import L
import time


# This class contains the search methods DFS and BFS.
# It creates a graph object, which contains the adjacency matrix
# and list of states.  
# Search contains the goal states.
# The initial states are set in the searches.
class Search:
    def __init__(self, problem):
        # the problem
        self.problem = problem
        # Though they are found, STRICT = True disallows reverse strings in output: 
        #                                   'hello world' but not 'world hello'
        self.STRICT = True

    # return Problem object
    def getProblem(self):
        return self.problem

    def _DFS_setup(self):
        openList = dq()
        openList.append( ( i for i in [self.problem.get_startState()] ) )
        return openList

    def _get_current_state(self, openList, closedList, results, dev=False):
        proceed = False
        
        while not proceed:
            try:
                #print(f'openList: {openList}\ntype(openList): {type(openList)}\n\ntype(openList[0]): {type(openList[0])}\nopenList[0]: {openList[0]}')
                # use next() to get the next node from the current generator
                current_state = next(openList[0])
                #print(current_state)
                proceed = True 
                # if we get a StopIteration:
            except StopIteration:
               # print(f'stopIteration..')
                # pop off this dead generator and resume the process.  
                openList.popleft()
                proceed = False
            # Return results if openList is empty
            except IndexError:
               # print(f'IndexError, return results....')
                if dev:
                    return results
                return [i for i in results if len([j for j in i if j != ' ']) == sum(list(self.problem.get_startState().name.values()))]
        # if we make it here return current state        
        return current_state

    
    #def checkDoubles(self, anagram):
         


    # Impolement for your stupid generator idea
    # 
    # 
    # 
    def DFS(self):
        results = list()
        closedList = list()
        # add start state to openlist
        openList = self._DFS_setup()
        skip = 1
        while True:
            # get current state
            current_state = self._get_current_state(openList, closedList, results)
           # print(f'\n=========\nWe are in the main search now...')
            if isinstance(current_state, list):
                print(f'The search has endeddddddddddd!')
                return current_state
           # print(f'and the current node has anagram: \n\t{current_state.get_anagram()}')
           # print(f'and the current pool has size: {len(current_state.pool)}')
            # We have current state and need to check termination 
            # if ppol is empty check that counter is also empty.  
            # If not its bad if so its good.
            if self.problem.goalTest(current_state):
               # print(f'Empty pool!')
                # if good collect the path and add it to the list of paths
                if current_state.name == {}:
                    t = set(current_state.get_anagram()) 
                    if t not in [set(i.split(' ')) for i in results]:
                   # print(f"Appending new anagram to output:{' '.join(current_state.get_anagram())}")
                        results.append(' '.join(current_state.get_anagram()))
                closedList.append(current_state)
            else:
                # if not generate this node's children generator 
                children = self.problem.generateChildren(current_state)
               
                # add this state to the closed list
                closedList.append(current_state)
                # add this new generator to the front of the openlist
                openList.insert(0,children)







    def BFS(self):
        results = []
        closedList = list()
        # add start state to openlist
        openList = self._DFS_setup()
        skip = 1
        while True:
            # get current state
            current_state = self._get_current_state(openList, closedList, results)
            if isinstance(current_state, list):
                return current_state
            
            # We have current state and need to check termination 
            # if ppol is empty check that counter is also empty.  
            # If not its bad if so its good.
            if self.problem.goalTest(current_state):
                # if good collect the path and add it to the list of paths
                if current_state.name == {}:
                    results.append(' '.join(current_state.get_anagram()))
                closedList.append(current_state)
            else:
                # if not generate this node's children generator 
                children = self.problem.generateChildren(current_state)
               
                # add this state to the closed list
                closedList.append(current_state)
                # add this new generator to the front of the openlist
                openList.append(children)

        






































    # These are for reference
    # 
    #
    #
    #
    #
    #
    #
    ##
    # 
    #     
    # Depth-first search
    def OldDFS(self):
        # openList is a python deque
        openList = dq()
        # initialize openList
        openList.append(self.problem.startState)
        # closed list initially empty
        closedList = []
        
        # while the open list isn't empty:
        while (len(openList) != 0):
            # Remove leftmost state from openList, call it currentState
            currentState = openList.popleft()

            # if currentState is a goal return Success and print frontier
            if(currentState.getData() in self.problem.goalStates.getData()):
                closedList.append(currentState)
                print("SUCCESS")
                self.problem.printData(closedList)
                return 1
            else:
                # get children of currentState with problem's 'generateStates' function.
                children = self.problem.generateChildren(currentState)

                # reverse children so search proceeds left to right    ## Seems like a bug
                children.reverse() 

                # put currentState on closed list
                closedList.append(currentState)

                # discard children of currentState if already on openList or closedList
                for child in children:
                    if child not in openList and child not in closedList:
                        # put remaining children on LEFT end of openList
                        openList.appendleft(child)

        # If search fails, tell the user and display final data
        print("FAIL")
        self.problem.printData(closedList)
        return 0



    # Breadth-first search
    def OldBFS(self):
        # openList is a python deque
        openList = dq()
        # initialize openList
        openList.append(self.problem.startState)
        # closed list initially empty
        closedList = []
        
        # while the open list isn't empty:
        while (len(openList) != 0):
            # Remove leftMost state from openList, call it currentState
            currentState = openList.popleft()

            # if currentState is a goal return Success and print frontier
            if(currentState.getData() in self.problem.goalStates.getData()):
                closedList.append(currentState)
                print("SUCCESS")
                self.problem.printData(closedList)
                return 1
            else:
                # get children of currentState with problem's 'generateStates' function.
                children = self.problem.generateStates(currentState)

                # put leftMost in closed using append
                closedList.append(currentState)

                # discard children of currentState if already on openList or closedList
                for child in children:
                    if child not in openList and child not in closedList:
                        # put remaining children on RIGHT end of openList
                        openList.append(child)

        # If search fails, tell the user and display final data
        print("FAIL")
        self.problem.printData(closedList)
        return 0

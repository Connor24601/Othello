import othelloBoard
from typing import Tuple, Optional

'''You should modify the chooseMove code for the ComputerPlayer
class. You should also modify the heuristic function, which should
return a number indicating the value of that board position (the
bigger the better). We will use your heuristic function when running
the tournament between players.

Feel free to add additional methods or functions.'''

class HumanPlayer:
    '''Interactive player: prompts the user to make a move.'''
    def __init__(self,name,color):
        self.name = name
        self.color = color
        
    def chooseMove(self,board):
        while True:
            try:
                move = eval('(' + input(self.name + \
                 ': enter row, column (or type "0,0" if no legal move): ') \
                 + ')')

                if len(move)==2 and type(move[0])==int and \
                   type(move[1])==int and (move[0] in range(1,9) and \
                   move[1] in range(1,9) or move==(0,0)):
                    break

                print('Illegal entry, try again.')
            except Exception:
                print('Illegal entry, try again.')

        if move==(0,0):
            return None
        else:
            return move

def heuristic(board) -> int:
    '''the heuristic that's used'''
    return movesHeuristic(board)


def basicHeuristic(board) -> int:
    '''This very silly heuristic just adds up all the 1s, -1s, and 0s
    stored on the othello board.'''
    sum = 0
    for i in range(1,othelloBoard.size-1):
        for j in range(1,othelloBoard.size-1):
            sum += board.array[i][j]
    return sum

def edgeHeuristic(board) -> int:
    '''values edges and corners more'''
    total = 0
    for i in range(1,othelloBoard.size-1):
        for j in range(1,othelloBoard.size-1):
            factor = 1
            if i == 1 or i == 8:
                factor += .3
            if j==1 or j==8:
                factor += .3
            total += board.array[i][j] * factor
    return total

def movesHeuristic(board) -> int:
    '''this just works?'''
    return len(board._legalMoves(1))-len(board._legalMoves(-1))




class ComputerPlayer:
    '''Computer player: chooseMove is where the action is.'''
    def __init__(self,name,color,heuristic,plies) -> None:
        self.name = name
        self.color = color
        self.heuristic = heuristic
        self.plies = plies

    def minimax(self, board, depth, isMax):
        if not board._legalMoves(self.color) or not depth:
            return (None,self.heuristic(board))
        
        best = (None,(-1)**isMax * 1E10) # get rekt dave

        for move in board._legalMoves(isMax * 2 - 1):
            possibleMove = self.minimax(board.makeMove(*move,isMax * 2 - 1),depth-1, not isMax)
            if isMax and possibleMove[1] > best[1]:
                best = (move,possibleMove[1])
            elif (not isMax) and possibleMove[1] < best[1]:
                best = (move,possibleMove[1])
        return best


    # chooseMove should return a tuple that looks like:
    # (row of move, column of move, number of times heuristic was called)
    # We will be using the third piece of information to assist with grading.
    def chooseMove(self,board) -> Optional[Tuple[int,int,int]]:
        '''This very silly player just returns the first legal move
        that it finds.'''

        return self.minimax(board,self.plies,(self.color+1) and True)[0] 
        

class ComputerPlayerPruning:
    def __init__(self,name,color,heuristic,plies) -> None:
        self.name = name
        self.color = color
        self.heuristic = heuristic
        self.plies = plies

    def minimax(self, board, depth, isMax,a,b):
        if not board._legalMoves(self.color) or not depth:
            return (None,self.heuristic(board))
        
        best = (None,(-1)**isMax * 1E10) # get rekt dave

        for move in board._legalMoves(isMax * 2 - 1):
            possibleMove = self.minimax(board.makeMove(*move,isMax * 2 - 1),depth-1, not isMax,a,b)
            
            if isMax and possibleMove[1] > best[1]:
                best = (move,possibleMove[1])
                a = max(best[1],a)
            elif (not isMax) and possibleMove[1] < best[1]:
                best = (move,possibleMove[1])
                b = min(best[1],b)

            if isMax and b <= best[1]:
                return best
            if (not isMax) and a >= best[1]:
                return best

        return best


    # chooseMove should return a tuple that looks like:
    # (row of move, column of move, number of times heuristic was called)
    # We will be using the third piece of information to assist with grading.
    def chooseMove(self,board) -> Optional[Tuple[int,int,int]]:
        '''This very silly player just returns the first legal move
        that it finds.'''

        return self.minimax(board,self.plies,(self.color+1) and True, -1E10, 1E10)[0] 
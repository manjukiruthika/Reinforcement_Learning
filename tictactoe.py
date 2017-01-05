'''
Created on 4 Jan 2017
Classic RL example - tictactoe
@author: manju.rangam
'''
import os
from random import randint

# Make table, one for each possible state of the game
states = []
V = []
totalStates = 0

board = [0,0,0,0,0,0,0,0,0]
          
tiles = [0,1,2]

def hasWinner(_board):
    for player in range(1, 3):
        #print('player', player)
        tile = tiles[player]
        #print('tile',tile)
      
        for i in range(0, 3):
            i = i * 3
            if (_board[i]     == tile) and \
               (_board[i + 1] == tile) and \
               (_board[i + 2] == tile):
                    return 1
                      
        # check vertical
        for i in range(0, 3):
            if (_board[i]     == tile) and \
               (_board[i + 3] == tile) and \
               (_board[i + 6] == tile):
                    return 1                      

        # check backward diagonal
        if (_board[0] == tile) and \
           (_board[4] == tile) and \
           (_board[8] == tile):
            return 1

        # check forward diagonal
        if (_board[6] == tile) and \
           (_board[4] == tile) and \
           (_board[2] == tile):
            return 1

    # check for draw
    for i in range(0, 9):
        # 0 estimated probability of winning
        if _board[i] == 0:
            return 0 

    # -1 is for draw match
    return -1

def determineValue(_board, player):
    won = hasWinner(_board)
    if 1==won:
        if 1==player:
            return 1.0
        else:
            return 0.0
    elif -1==won:
        return 0.0
    else:
        return 0.5


def switchPlayer(player):
    if player == 1:
        return 2
    else:
        return 1

def initBoard():
    for i in range(0,9):
        board[i] = 0

def getListOfBlankTiles():
    blanks = []
    for i in range(0, 9):
        if board[i] == 0:
            blanks.append(i)
    return blanks

# Need to recheck algorithm for getting all states
def createAllStates(board, player):
    won = hasWinner(board)
    print("won", won)
    global count 

    if won == 1 or won == -1:
        return
    else:
        for i in range(0, 9):
            if board[i] == 0:
                board[i] = player
                if board[:] not in states:
                    states.append(board[:])
                    print("board", board[:])
                    V.append(determineValue(board, player))
                createAllStates(board[:], switchPlayer(player))
                print("board after player change", board[:])
                board[i] = 0
                    
def loadStatesFromFile(fp):
    global totalStates
    while True:
        line = fp.readline()
        if line == "":
            break
        first_split = line.split(' ')
        state = map(int,first_split[0].split(':'))
        value = float(first_split[1])
        states.append(state)
        V.append(value)
        totalStates = totalStates + 1
        
def printBoard(_board):
    size = len(_board)
    for index in range(0, size):
        if _board[index] == 1:
            print 'X',
        elif _board[index] == 2:
            print 'O',
        else:
            print '_',
        if 0 == ((index + 1) % 3):
            print        

# State-Value Function V(s)
# V(s) = V(s) + alpha [ V(s') - V(s) ]
# s  = current state
# s' = next state
# alpha = learning rate
def updateEstimateValueOfS(sPrime, s):
    V[s] = V[s] + alpha*(V[sPrime] - V[s])


def greedyMove(player):
    maxVal = 0
    maxIndex = 0
   
    nextMoves = getListOfBlankTiles()
    print("nextMoves", nextMoves)
    boardIndex = nextMoves.pop()
    print("boardindex", boardIndex)
    board[boardIndex] = player
    print(board)
    maxIndex = states.index(board)
    maxVal = V[maxIndex] 
    board[boardIndex] = 0    
    
    for i in nextMoves:
        board[i] = player
        idx = states.index(board)    
        if V[idx] > maxVal:
            boardIndex = i
            maxIndex = idx
            maxVal = V[idx]
        board[i] = 0

    print("board index, maxIndex", boardIndex, maxIndex)
    return boardIndex, maxIndex


def updateBoard(_board, player, index):
    if _board[index] == 0:
        _board[index] = player
        return True
  
    return False

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# PROGRAM STARTS HERE
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# step-size parameter (rate of learning)
alpha = 0.01

# exploration rate
exploreRate = 0.1

filename = "tictactoe.dat"
# Create table of all possible TicTacToe states
if os.path.isfile(filename):
    fp = open(filename, "r")
    print "Building states from file..."
    loadStatesFromFile(fp)
    fp.close()
else:
    print "Building states from scratch..."
    createAllStates(board, 1)
    createAllStates(board, 2)
totalStates = len(V)
print "Total States: %d" %(len(states))

playTimes = 0      # number of plays during Learning Phase
numPlayer1Won = 0       # number of games won Player 1
numPlayer2Won = 0       # number of games won Player 2
numDraws = 0            # number of draws
player = 1              # starts with Player 1 during Learning Phase

''' Loop '''
count = 1
while (count < 2):
    count = count+1
    # ensure board is all zeroes
    initBoard()
  
    # player 1 = 1 and player 2 = 2
    if playTimes:
        # Learning phase:
        # computer plays as player 1 or 2 equal number of times
        player = switchPlayer(player)
    else:
        # Game phase:
        # randomly select who goes first
        player = randint(1,2)
    
    print( "Player playing", player)    
    # Prints board only on Game phase
    if not playTimes:
        print "Player 1 = Computer"
        print "Player 2 = You!"
    
    prevIndex = 0          # previous state index
    maxIndex = 0           # index with maximum state value
    firstPlay = True       # flag for first play of a game episode
    
    printBoard(board)
    print

    while (True):
        print("get next moves")
        nextMoves = getListOfBlankTiles()
        countNextMoves = len(nextMoves)
        #print(countNextMoves) 
        ex = randint(1, 100)/100.0
        if ex <= exploreRate:
            userPlay = nextMoves[randint(0, countNextMoves - 1)]
            boardIndex= userPlay
            board[boardIndex] = player
            maxIndex = states.index(board)
            print ("Exploratory user Play", userPlay)
        else:
            userPlay, maxIndex = greedyMove(player)
            print("Greedy move userPlay", userPlay)
            
        if not firstPlay:
            print "V(s) = %f changed to" %(V[prevIndex]),
            updateEstimateValueOfS(maxIndex, prevIndex)
            print "V(s) = %f" %(V[prevIndex])
        prevIndex = maxIndex
        
        # player 1 has done one play
        firstPlay = False            
        
        updateBoard(board, player, userPlay)
        
        printBoard(board)
    
        won = hasWinner(board)
        
        if 1 == won:
            if 1 == player:
                numPlayer1Won = numPlayer1Won + 1
            else:
                numPlayer2Won = numPlayer2Won + 1
                
            print "Player %d has won!" %(player) 
            print
            break
    
        if -1 == won:
            numDraws = numDraws + 1
            #maxIndex = states.index(board)
            #print "V(s) = %f changed to" %(V[prevIndex]),
            #updateEstimateValueOfS(maxIndex, prevIndex)
            #print "V(s) = %f" %(V[prevIndex])
            print "It's a draw!"
            print
            break        
        player = switchPlayer(player)
        print('switching player')
'''
These fuctions define an AI that uses the Minimax algorithm 
to figure out what moves to make.  This is a very complex class.

The makeMove(Board b) method takes a board, generates possible boards based on the 
possible moves of the AI, and has those boards evaluated by the evaluatePosition function.
The board that scores the highest becomes the next move, and the doMove(Board b, Move moveToMake)
method is invoked, which performs that move on the board.

The evaluatePosition function is recursive and generates a game tree which it searches to figure
out how advantageous a board it is.  It uses the MinMax algorithm with alpha-beta pruning to 
rate moves, and when a node at the depth specified by the constant DEPTH is reached,
the evaluate function is called to determine the ultimate worth of that board. This is
then propagated up through the game tree to determine how advantageous a move is.  
'''

'''
The X() method generates all the possible AI moves
(note again that the AI is always black). It then calls the evaluatePosition function on each
possible board to figure out the best move.  
 
@return a string describing the move that was made
'''
def hueristicX(self):

    boardToMakeMoveOn = self.copy()
    moves = [] #keeps track of all possible moves
    possibleBoards = [] #keeps track of the possible boards (boards with the possible moves made on them)
    x = 0
    '''
    iterates through board, generates all possible moves and saves them in moves
    '''
    for i in range(0,64):
       if self.piece_type_at(i) != None:
           piece = self.piece_at(i)
           if piece.color == True:
               for j in range(0,64):
                    move = Move(i,j)
                    if(self.is_pseudo_legal(move)):
                        print "Legal move:",self.piece_at(i),"for move:",move.uci()
                        moves.append(move.uci())
                        board = self.copy() #calls the copy constructor of the board class
                       try:
                            board.push_san(move.uci())//performs move on the new board
                            possibleBoards.append(board)
                        except ValueError:
                            print('')
    #initializes bestMove to the first move in the                    
    bestMove = moves[0]
    bestMoveScore = self.evaluatePosition(possibleBoards[0], sys.float_info.min, sys.float_info.max, DEPTH, False)

    #call evaluateposition on each move
    #keep track of the move with the best score
    for i in range(1,len(possibleBoards)):
        print "Evaluating move:",moves[i]
        '''
         * calls evaluatePosition on each possible board and if the score is higher than previous,
         * reset the bestMove
        '''
        j = self.evaluatePosition(possibleBoards[i], sys.float_info.min, sys.float_info.max, DEPTH, False)
        if(j >= bestMoveScore):
            bestMove = moves[i]
            bestMoveScore = j

    return bestMove

'''
The Y() method generates all the possible AI moves
(note again that the AI is always black). It then calls the evaluatePosition function on each
possible board to figure out the best move.  

@return a string describing the move that was made
'''
def hueristicY(self):
    boardToMakeMoveOn = self.copy()
    moves = [] #keeps track of all possible moves
    possibleBoards = [] #keeps track of the possible boards (boards with the possible moves made on them)
    x = 0
    '''
    iterates through board, generates all possible moves and saves them in moves
    '''
    for i in range(0,64):
       if self.piece_type_at(i) != None:
           piece = self.piece_at(i)
           if piece.color == False:
               for j in range(0,64):
                    move = Move(i,j)
                    if(self.is_pseudo_legal(move)):
                        print "Legal move:",self.piece_at(i),"for move:",move.uci()
                        moves.append(move.uci())
                        board = self.copy() #calls the copy constructor of the board class
                        try:
                            board.push_san(move.uci()) #performs move on the new board
                            possibleBoards.append(board)
                        except ValueError:
                            print('')
    bestMove = moves[0]
    bestMoveScore = self.evaluatePosition(possibleBoards[0], sys.float_info.min, sys.float_info.max, DEPTH, False)

    for i in range(1,len(possibleBoards)):
        print "Evaluating move:",moves[i]
        j = self.evaluatePosition(possibleBoards[i], sys.float_info.min, sys.float_info.max, DEPTH, False)
        if(j >= bestMoveScore):
            bestMove = moves[i]
            bestMoveScore = j

    return bestMove

'''
The doMove(Board b, Move moveToMake) performs the Move moveToMake on the board provided in the 
parameters. It returns a string describing the move that was made.  
 
@param board
@param moveToMake
@return string describing what kind of move was made
'''
def doMove(self, board, moveToMake):
    piece = board.piece_at(moveToMake)

    board.remove_piece_at(moveToMake)
    board.set_piece_at(moveToMake)

'''
The evaluatePosition function takes a board, initial alpha, initial beta, depth, and color as parameters
and computes a number that describes how advantageous for the AI a particular board is.  The function is 
recursive, and every time it evaluates itself it decreases the depth by 1.  When the depth reaches 0, the
function returns the result of running the evaluate function on the board.  If the depth is not 0, the function
generates all possible moves from that position for the color specified, and then runs evaluatePosition for 
each of the boards generated by each possible move. 
@param board
@param alpha
@param beta 
@param depth
@param color
@return an int giving a score of how good a particular board is, with higher numbers corresponding to better boards for the AI
'''
def evaluatePosition(self, board, alpha, beta, depth, color):
    print "Begin evaluating postion: depth-",depth,"for-",color
    '''
    Base case: when depth is decremented to 0, evaluatePosition simply returns the result
    of the evaluate function
    '''
    if(depth == 0):
        evaluation = self.evaluate(board)
        print "Evaluated to:",evaluation
        return evaluation

    if(color == False): #minimizing player--sequence of events that occurs
        moves = [] #this arraylist keeps track of possible moves from the given position
        '''
        Iterate through the board, collect all possible moves of the minimizing player
        '''

        for i in range(0,64):
            if self.piece_type_at(i) != None:
                piece = self.piece_at(i)
                if piece.color == color:
                    for j in range(0,64):
                        move = Move(i,j)
                        if(board.is_pseudo_legal(move)):
                            moves.append(move.uci()) #adds moves to the arraylist as they are calculated
        '''
        This for loop goes through all possible moves and calls evaluatePosition on them,
        changing the color.  Alpha-beta pruning is used here to remove obviously poor moves.
        These are determined by the variables alpha and beta.  All moves where the beta,
        which is the score of the minimizing (in this case white player) is less than or
        equal to alpha are discarded.  
        '''                    
        newBeta = beta
        for move in moves://for child in node
            print "Move to be evaluated:",move
            sucessorBoard = board.copy()
            try:
                sucessorBoard.push_san(move)
            except ValueError:
                print('')
            newBeta = min(newBeta, self.evaluatePosition(sucessorBoard, alpha, beta, DEPTH - 1, not color))
            if(newBeta <= alpha):
                break
        return newBeta #returns the highest score of the possible moves
    else: #maximizing player--this is the course of action determined if this is the maximizing player, or black
        moves = []
        '''
        These for loops iterate through the board and add all possible pieces to the ArrayList of
        moves.  
        '''
        for i in range(0,64):
            if self.piece_type_at(i) != None:
                piece = self.piece_at(i)
                if piece.color == WHITE:
                    for j in range(0,64):
                        move = Move(i,j)
                        if(self.is_pseudo_legal(move)):
                            moves.append(move.uci()) 
        '''
        This for loop cycles through all possible moves and 
        calculates a new alpha if the successor board evaluates
        to a higher number than what is currently the highest score,
        which is stored in alpha.  
        '''
        newAlpha = alpha
        for move in Moves:
            sucessorBoard = board.copy()
            try:
                sucessorBoard.push_san(move.uci())
            except ValueError:
                print('')
            newAlpha = min(newAlpha, evaluatePosition(successorBoard, alpha, beta, DEPTH - 1, not color)) #think about how to change moves
            if(beta <= newAlpha):
                break
        return newAlpha #returns the highest score of the possible moves

'''
The evaluate(Board b) function is an evaluation function that returns a number based on
how advantageous a board is for the maximizing, black in this case, player. This function
simply iterates through the whole board and gives a weighted number to each piece on the board,
kings naturally yielding the highest number, queens the second, and so on.  The total white score
is subtracted from the total black score to give a full picture of how advantageous the board is 
for a black player.  
@param board
@return int that represents how advantageous a board is
'''
def evaluate(self, board):
    whiteScore = 0
    blackScore = 0

    for i in range(0,64):
        if board.piece_type_at(i) != None:
            piece = board.piece_at(i)
            if piece.color == WHITE:
                if board.piece_type_at(i) == 5:
                    whiteScore += 9
                elif board.piece_type_at(i) == 4:
                    whiteScore += 5
                elif board.piece_type_at(i) ==  6 | board.piece_type_at(i) == 3:
                    whiteScore += 3
                elif board.piece_type_at(i) == 1:
                    whiteScore += 1
                elif board.piece_type_at(i) == 6:
                    whiteScore += 10000000
            elif piece.color == BLACK:
                if board.piece_type_at(i) == 5:
                    blackScore += 9
                elif board.piece_type_at(i) == 4:
                    blackScore += 5
                elif board.piece_type_at(i) ==  6 | board.piece_type_at(i) == 3:
                    blackScore += 3
                elif board.piece_type_at(i) == 1:
                    blackScore += 1
                elif board.piece_type_at(i) == 6:
                    whiteScore += 10000000
    return blackScore-whiteScore

from connectfour.agents.computer_player import RandomAgent
import random, copy

class StudentAgent(RandomAgent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 1


    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        Returns:
            A tuple of two integers, (row, col)
        """

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            next_state = board.next_state(self.id, move[1])
            moves.append( move )
            vals.append( self.dfMiniMax(next_state, 1) )

        bestMove = moves[vals.index( max(vals) )]
        return bestMove

    def dfMiniMax(self, board, depth):
        # Goal return column with maximized scores of all possible next states

        if depth == self.MaxDepth:
            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            if depth % 2 == 1:
                next_state = board.next_state(self.id % 2 + 1, move[1])
            else:
                next_state = board.next_state(self.id, move[1])

            moves.append( move )
            vals.append( self.dfMiniMax(next_state, depth + 1) )


        if depth % 2 == 1:
            bestVal = min(vals)
        else:
            bestVal = max(vals)

        return bestVal

    def evaluateBoardState(self, board):
        totalHeuristics = totalOldHeuritics = heuristics = oldMax = 0
        newMax, newMin = 1, -1

        if self.winner(board) == self.id % 2 + 1:
            return -1
        if self.winner(board) == self.id:
            return 1

        heuristic, oldMax = self.agent(board)
        totalHeuristics += heuristic
        totalOldHeuritics += oldMax

        heuristic, oldMax = self.inline4(board)
        totalHeuristics += heuristic
        totalOldHeuritics += oldMax

        oldRange = oldMax - (0 - totalOldHeuritics)
        newRange = newMax - newMin
        value = (((totalHeuristics - (0 - totalOldHeuritics)) * newRange) / oldRange) + newMin

        return value

    def agent(self, board):
        heuristic = max = 0
        centreCol = 3
        centreColScr = 8
        _2n4colScr = 4
        _1n5colScr = 2

        for x in range(board.height):
            if board.get_cell_value(x, centreCol) == self.id:
                heuristic += centreColScr
            if board.get_cell_value(x, centreCol) == self.id % 2 + 1:
                heuristic -= centreColScr

            if board.get_cell_value(x, 2) == self.id or board.get_cell_value(x, 4) == self.id:
                heuristic += _2n4colScr
            if board.get_cell_value(x, 2) == self.id % 2 + 1 or board.get_cell_value(x, 4) == self.id % 2 + 1:
                heuristic -= _2n4colScr

            if board.get_cell_value(x, 1) == self.id or board.get_cell_value(x, 5) == self.id:
                heuristic += _1n5colScr
            if board.get_cell_value(x, 1) == self.id % 2 + 1 or board.get_cell_value(x, 5) == self.id % 2 + 1:
                heuristic -= _1n5colScr

        max = (centreColScr * board.height) + _2n4colScr * board.height * (2.0 + _1n5colScr) * board.height * 2.0

        return heuristic, max

    def inline4(self, board):
        heuristic = 0
        pointsForHor2 = pointsForVert2 = pointsForDiag2 = 3
        pointsForHor3 = pointsForVert3 = pointsForDiag3 = 30

        maxHor, maxVer, maxDiag = pointsForHor3 * 4 * board.height, pointsForVert3 * 3 * board.width, pointsForDiag3 * 4 * 3 * 2

        max = maxHor + maxVer + maxDiag

        heuristic += self.horizontalCheck(board, pointsForHor2, pointsForHor3)
        heuristic += self.verticalCheck(board, pointsForVert2, pointsForVert3)
        heuristic += self.diagonalCheck(board, pointsForDiag2, pointsForDiag3)

        return heuristic, max

    def horizontalCheck(self, board, points2, points3):
        heuristic, numOfToken, waysConnect4 = 0, 0, 4
        inline4 = True

        for row in range(board.height):
            start, end = 0, 4
            for i in range(waysConnect4):
                for col in range(start + i, end + i):
                    if board.get_cell_value(row, col) == self.id % 2 + 1:
                    	inline4 = False
                    	break
                    if board.get_cell_value(row, col) == self.id:
                        numOfToken += 1

                if inline4 == False:
                	numOfToken = 0
                	inline4 = True
                	continue
                if numOfToken == 2:
                    heuristic += points2
                if numOfToken == 3:
                    heuristic += points3
                numOfToken = 0

        inline4 = True
        numOfToken = 0
        for row in range(board.height):
            start, end = 0, 4
            for i in range(waysConnect4):
                for col in range(start + i, end + i):
                    if board.get_cell_value(row, col) == self.id:
                    	inline4 = False
                    	break
                    if board.get_cell_value(row, col) == self.id % 2 + 1:
                        numOfToken += 1

                if inline4 == False:
                    numOfToken = 0
                    inline4 = True
                    continue
                if numOfToken == 2:
                    heuristic -= points2
                if numOfToken == 3:
                    heuristic -= points3
                numOfToken = 0

        return heuristic

    def verticalCheck(self, board, points2, points3):
        heuristic, numOfToken, waysConnect4 = 0, 0, 3
        inline4 = True

        for col in range(board.width):
            start, end = 0, 4
            for i in range(waysConnect4):
                for row in range(start + i, end + i):
                    if board.get_cell_value(row, col) == self.id % 2 + 1:
                        inline4 = False
                        break
                    if board.get_cell_value(row, col) == self.id:
                        numOfToken += 1

                if inline4 == False:
                    numOfToken = 0
                    inline4 = True
                    continue
                if numOfToken == 2:
                    heuristic += points2
                if numOfToken == 3:
                    heuristic += points3
                numOfToken = 0

        inline4 = True
        numOfToken= 0
        for column in range(board.width):
            start, end = 0, 4
            for i in range(waysConnect4):
                for row in range(start + i, end + i):
                    if board.get_cell_value(row, col) == self.id:
                        inline4 = False
                        break
                    if board.get_cell_value(row, col) == self.id % 2 + 1:
                        numOfToken += 1

                if inline4 == False:
                    numOfToken = 0
                    inline4 = True
                    continue
                if numOfToken == 2:
                    heuristic -= points2
                if numOfToken == 3:
                    heuristic -= points3
                numOfToken = 0

        return heuristic

    def diagonalCheck(self, board, points2, points3):
        heuristic, numOfToken, waysConnect4 = 0, 0, 4
        inline4 = True

        for row in range(3):
            start, end = 0, 4
            for i in range(waysConnect4):
                rowOffset = 0
                for col in range(start + i, end + i):
                    if board.get_cell_value(row + rowOffset, col) == self.id % 2 + 1:
                        inline4 = False
                        break
                    if board.get_cell_value(row + rowOffset, col) == self.id:
                        numOfToken += 1
                    rowOffset += 1

                if inline4 == False:
                    numOfToken = 0
                    inline4 = True
                    continue
                if numOfToken == 2:
                    heuristic += points2
                if numOfToken == 3:
                    heuristic += points3
                numOfToken = 0

        inline4 = True
        numOfToken = 0
        for row in range(3):
            start, end = 0, 4
            for i in range(waysConnect4):
                rowOffset = 0
                for col in range(start + i, end + i):
                    if board.get_cell_value(row + rowOffset, col) == self.id:
                        inline4 = False
                        break
                    if board.get_cell_value(row + rowOffset, col) == self.id % 2 + 1:
                        numOfToken += 1
                    rowOffset += 1

                if inline4 == False:
                    numOfToken = 0
                    inline4 = True
                    continue
                if numOfToken == 2:
                    heuristic -= points2
                if numOfToken == 3:
                    heuristic -= points3
                numOfToken = 0

        for row in range(3, 6):
            start, end = 0, 4
            for i in range(waysConnect4):
                rowOffset = 0
                for col in range(start + i, end + i):
                    if board.get_cell_value(row - rowOffset, col) == self.id % 2 + 1:
                        inline4 = False
                        break
                    if board.get_cell_value(row - rowOffset, col) == self.id:
                        numOfToken += 1
                    rowOffset += 1

                if inline4 == False:
                    numOfToken = 0
                    inline4 = True
                    continue
                if numOfToken == 2:
                    heuristic += points2
                if numOfToken == 3:
                    heuristic += points3
                numOfToken = 0

        inline4 = True
        numOfToken = 0
        for row in range(3, 6):
            start, end = 0, 4
            for i in range(waysConnect4):
                rowOffset = 0
                for col in range(start + i, end + i):
                    if board.get_cell_value(row - rowOffset, col) == self.id:
                        inline4 = False
                        break
                    if board.get_cell_value(row - rowOffset, col) == self.id % 2 + 1:
                        numOfToken += 1
                    rowOffset += 1

                if inline4 == False:
                    numOfToken = 0
                    inline4 = True
                    continue
                if numOfToken == 2:
                    heuristic -= points2
                if numOfToken == 3:
                    heuristic -= points3
                numOfToken = 0

        return heuristic

    def winner(self, board):
        """
        Takes the board as input and determines if there is a winner.
        If the game has a winner, it returns the player number (Player One = 1, Player Two = 2).
        If the game is still ongoing, it returns zero.
        """
        row_winner = self._check_rows(board)
        if row_winner:
            return row_winner
        col_winner = self._check_columns(board)
        #print("col winner = ", col_winner)
        if col_winner:
            return col_winner
        diag_winner = self._check_diagonals(board)
        if diag_winner:
            return diag_winner
        return 0  # no winner yet

    def _check_rows(self, board):
        for row in board.board:
            same_count = 1
            curr = row[0]
            for i in range(1, board.width):
                if row[i] == curr:
                    same_count += 1
                    if same_count == board.num_to_connect and curr != 0:
                        return curr
                else:
                    same_count = 1
                    curr = row[i]
        return 0

    def _check_columns(self, board):
        for i in range(board.width):
            same_count = 1
            curr = board.board[0][i]
            for j in range(1, board.height):
                if board.board[j][i] == curr:
                    same_count += 1
                    if same_count == board.num_to_connect and curr != 0:
                        return curr
                else:
                    same_count = 1
                    curr = board.board[j][i]
        return 0

    def _check_diagonals(self, board):
        boards = [
            board.board,
            [row[::-1] for row in copy.deepcopy(board.board)]
        ]

        for b in boards:
            for i in range(board.width - board.num_to_connect + 1):
                for j in range(board.height - board.num_to_connect + 1):
                    if i > 0 and j > 0:  # would be a redundant diagonal
                        continue

                    # (j, i) is start of diagonal
                    same_count = 1
                    curr = b[j][i]
                    k, m = j + 1, i + 1
                    while k < board.height and m < board.width:
                            if b[k][m] == curr:
                                same_count += 1
                                if same_count is board.num_to_connect and curr != 0:
                                    return curr
                            else:
                                same_count = 1
                                curr = b[k][m]
                            k += 1
                            m += 1
        return 0

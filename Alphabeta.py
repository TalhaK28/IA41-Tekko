from Check_victory import check_victory

def ai_alphabeta(board, player_symbol, turn_count, max_depth=3):
    """Algorithme Alpha-Bêta pour IA de niveau moyen."""
    opponent_symbol = 'X' if player_symbol == 'O' else 'O'

    def evaluate_state(board):
        """Évalue l'état du plateau pour donner un score à l'IA."""
        if check_victory(board, player_symbol):
            return 1000
        if check_victory(board, opponent_symbol):
            return -1000

        score = 0
        for y in range(5):
            for x in range(5):
                if board[y][x] == player_symbol:
                    score += count_near_victories(board, y, x, player_symbol) * 1.5
                elif board[y][x] == opponent_symbol:
                    score -= count_near_victories(board, y, x, opponent_symbol)
        return score

    def count_near_victories(board, y, x, symbol):
        directions = [
            [(0, 1), (0, 2), (0, 3)],
            [(1, 0), (2, 0), (3, 0)],
            [(1, 1), (2, 2), (3, 3)],
            [(-1, 1), (-2, 2), (-3, 3)],
            [(0, 1), (1, 0), (1, 1)]
        ]

        count = 0
        for direction in directions:
            try:
                aligned = sum(
                    1 for dy, dx in direction if 0 <= y + dy < 5 and 0 <= x + dx < 5 and board[y + dy][x + dx] == symbol
                )
                if aligned >= 2:
                    count += aligned ** 2
            except IndexError:
                continue
        return count

    def alphabeta(board, depth, is_maximizing, alpha, beta, turn_count):
        if depth == 0 or check_victory(board, player_symbol) or check_victory(board, opponent_symbol):
            return evaluate_state(board)

        if is_maximizing:
            v = -float('inf')
            for move in generate_moves(board, player_symbol, turn_count):
                original_symbol = board[move[0][0]][move[0][1]] if move[0] else ' '
                apply_move(board, move, player_symbol)
                eval = alphabeta(board, depth - 1, False, alpha, beta, turn_count + 1)
                undo_move(board, move, original_symbol)
                v = max(v, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return v
        else:
            v = float('inf')
            for move in generate_moves(board, opponent_symbol, turn_count):
                original_symbol = board[move[0][0]][move[0][1]] if move[0] else ' '
                apply_move(board, move, opponent_symbol)
                eval = alphabeta(board, depth - 1, True, alpha, beta, turn_count + 1)
                undo_move(board, move, original_symbol)
                v = min(v, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return v

    def generate_moves(board, symbol, turn_count):
        moves = []
        if turn_count < 8:
            for y in range(5):
                for x in range(5):
                    if board[y][x] == ' ':
                        moves.append((None, (y, x)))
        else:
            for y in range(5):
                for x in range(5):
                    if board[y][x] == symbol:
                        for dy, dx in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < 5 and 0 <= nx < 5 and board[ny][nx] == ' ':
                                moves.append(((y, x), (ny, nx)))
        return moves

    def apply_move(board, move, symbol):
        if move[0] is None:
            y, x = move[1]
            board[y][x] = symbol
        else:
            (sy, sx), (dy, dx) = move
            board[dy][dx] = symbol
            board[sy][sx] = ' '

    def undo_move(board, move, original_symbol):
        if move[0] is None:
            y, x = move[1]
            board[y][x] = ' '
        else:
            (sy, sx), (dy, dx) = move
            board[sy][sx] = original_symbol
            board[dy][dx] = ' '

    if turn_count < 8:
        best_score = -float('inf')
        best_move = None
        for move in generate_moves(board, player_symbol, turn_count):
            apply_move(board, move, player_symbol)
            score = alphabeta(board, max_depth, False, -float('inf'), float('inf'), turn_count + 1)
            undo_move(board, move, player_symbol)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move[1]
    else:
        best_score = -float('inf')
        best_move = None
        for move in generate_moves(board, player_symbol, turn_count):
            apply_move(board, move, player_symbol)
            score = alphabeta(board, max_depth, False, -float('inf'), float('inf'), turn_count + 1)
            undo_move(board, move, player_symbol)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

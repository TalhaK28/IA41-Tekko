from Check_victory import check_victory

def ai_greedy(board, player_symbol, turn_count, max_depth=3):
    """Algorithme gourmand qui maximise le gain immédiat."""
    opponent_symbol = 'X' if player_symbol == 'O' else 'O'

    def evaluate_state(board):
        """Évalue l'état du plateau pour donner un score à l'IA."""
        if check_victory(board, player_symbol):
            return 1000
        if check_victory(board, opponent_symbol):
            return -1000

        score = 0

        # Analyse des opportunités pour l'IA
        for y in range(5):
            for x in range(5):
                if board[y][x] == player_symbol:
                    score += count_near_victories(board, y, x, player_symbol) * 1.5
                elif board[y][x] == opponent_symbol:
                    score -= count_near_victories(board, y, x, opponent_symbol)

        return score

    def count_near_victories(board, y, x, symbol):
        """Compte les configurations proches de victoire autour d'une case donnée."""
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

    def generate_moves(board, symbol):
        moves = []
        if turn_count < 8:  # Phase de placement
            for y in range(5):
                for x in range(5):
                    if board[y][x] == ' ':
                        moves.append((None, (y, x)))
        else:  # Phase de déplacement
            for y in range(5):
                for x in range(5):
                    if board[y][x] == symbol:
                        for dy, dx in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < 5 and 0 <= nx < 5 and board[ny][nx] == ' ':
                                moves.append(((y, x), (ny, nx)))
        return moves

    def apply_move(board, move, symbol):
        if move[0] is None:  # Placement
            y, x = move[1]
            board[y][x] = symbol
        else:  # Déplacement
            (sy, sx), (dy, dx) = move
            board[dy][dx] = symbol
            board[sy][sx] = ' '

    def undo_move(board, move, original_symbol):
        if move[0] is None:  # Annuler un placement
            y, x = move[1]
            board[y][x] = ' '
        else:  # Annuler un déplacement
            (sy, sx), (dy, dx) = move
            board[sy][sx] = original_symbol
            board[dy][dx] = ' '

    if turn_count < 8:
        best_score = -float('inf')
        best_move = None
        for move in generate_moves(board, player_symbol):
            apply_move(board, move, player_symbol)
            score = evaluate_state(board)
            undo_move(board, move, player_symbol)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move[1]
    else:
        best_score = -float('inf')
        best_move = None
        for move in generate_moves(board, player_symbol):
            apply_move(board, move, player_symbol)
            score = evaluate_state(board)
            undo_move(board, move, player_symbol)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

import random

def ai_easy(board, player_symbol):
    """Renvoie une position aléatoire disponible pour l'IA facile."""
    empty_cells = [(r, c) for r in range(len(board)) for c in range(len(board[r])) if board[r][c] == ' ']
    if empty_cells:
        return random.choice(empty_cells)
    return None

def check_victory(board, symbol):
    """Vérifie si un joueur a gagné."""
    rows = len(board)
    cols = len(board[0])

    # Vérification des lignes
    for i in range(rows):
        for j in range(cols - 3):
            if all(board[i][j + k] == symbol for k in range(4)):
                return True

    # Vérification des colonnes
    for i in range(rows - 3):
        for j in range(cols):
            if all(board[i + k][j] == symbol for k in range(4)):
                return True

    # Vérification des diagonales descendantes
    for i in range(rows - 3):
        for j in range(cols - 3):
            if all(board[i + k][j + k] == symbol for k in range(4)):
                return True

    # Vérification des diagonales montantes
    for i in range(3, rows):
        for j in range(cols - 3):
            if all(board[i - k][j + k] == symbol for k in range(4)):
                return True

    # Vérification des carrés 2x2
    for i in range(rows - 1):
        for j in range(cols - 1):
            if board[i][j] == symbol and board[i][j + 1] == symbol and \
               board[i + 1][j] == symbol and board[i + 1][j + 1] == symbol:
                return True

    return False

def ai_hard_minmax(board, player_symbol, turn_count, max_depth=3):
    """Algorithme Minimax pour IA difficile avec élagage alpha-bêta."""
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
                    score += count_near_victories(board, y, x, player_symbol) * 1.5  # Favoriser l'attaque
                elif board[y][x] == opponent_symbol:
                    score -= count_near_victories(board, y, x, opponent_symbol)  # Défense

        return score

    def count_near_victories(board, y, x, symbol):
        """Compte les configurations proches de victoire autour d'une case donnée."""
        directions = [
            [(0, 1), (0, 2), (0, 3)],  # Ligne droite
            [(1, 0), (2, 0), (3, 0)],  # Colonne
            [(1, 1), (2, 2), (3, 3)],  # Diagonale descendante
            [(-1, 1), (-2, 2), (-3, 3)],  # Diagonale montante
            [(0, 1), (1, 0), (1, 1)]   # Carré 2x2
        ]

        count = 0
        for direction in directions:
            try:
                aligned = sum(
                    1 for dy, dx in direction if 0 <= y + dy < 5 and 0 <= x + dx < 5 and board[y + dy][x + dx] == symbol
                )
                if aligned >= 2:
                    count += aligned ** 2  # Prioriser des configurations plus avancées
            except IndexError:
                continue

        return count

    def minimax(board, depth, is_maximizing, alpha, beta):
        if depth == 0 or check_victory(board, player_symbol) or check_victory(board, opponent_symbol):
            return evaluate_state(board)

        if is_maximizing:
            v = -float('inf')
            for move in generate_moves(board, player_symbol):
                original_symbol = board[move[0][0]][move[0][1]] if move[0] else ' '
                apply_move(board, move, player_symbol)
                eval = minimax(board, depth - 1, False, alpha, beta)
                undo_move(board, move, original_symbol)
                v = max(v, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return v
        else:
            v = float('inf')
            for move in generate_moves(board, opponent_symbol):
                original_symbol = board[move[0][0]][move[0][1]] if move[0] else ' '
                apply_move(board, move, opponent_symbol)
                eval = minimax(board, depth - 1, True, alpha, beta)
                undo_move(board, move, original_symbol)
                v = min(v, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return v

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
            score = minimax(board, max_depth, False, -float('inf'), float('inf'))
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
            score = minimax(board, max_depth, False, -float('inf'), float('inf'))
            undo_move(board, move, player_symbol)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move
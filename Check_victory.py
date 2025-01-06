# Description: Fonction permettant de vérifier si un joueur a gagné.
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


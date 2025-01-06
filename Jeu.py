import pygame
import sys
from Check_victory import check_victory
from Easy_ia import ai_greedy
from MinMax import ai_minmax
from Alphabeta import ai_alphabeta
from Menu import TeekoMenu

# Paramètres globaux
CELL_SIZE = 120
BOARD_SIZE = 5
GRID_SIZE = CELL_SIZE * BOARD_SIZE
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
MARGIN = (WINDOW_WIDTH - GRID_SIZE) // 2

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BACKGROUND_COLOR = (50, 50, 50)

class TeekoGamePygame:
    def __init__(self, mode, difficulty=None):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Teeko Game")
        self.font = pygame.font.Font(None, 50)

        # Initialiser les données du jeu
        self.board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.player_symbols = ['X', 'O']
        self.current_player = 0
        self.player_pieces = {'X': [], 'O': []}
        self.turn_count = 0
        self.selected_piece = None

        # Stocker le mode et la difficulté
        self.mode = mode
        self.difficulty = difficulty

        # Ajouter un état pour gérer la popup
        self.popup_active = False

    def draw_board(self):
        """Dessine le plateau et les éléments de l'interface."""
        self.screen.fill(BACKGROUND_COLOR)

        # Texte du joueur actuel
        player_text = f"Tour du joueur {self.current_player + 1} ({self.player_symbols[self.current_player]})"
        player_surface = self.font.render(player_text, True, WHITE)
        self.screen.blit(player_surface, ((WINDOW_WIDTH - player_surface.get_width()) // 2, 20))

        # Dessiner la grille
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x, y = MARGIN + col * CELL_SIZE, 100 + row * CELL_SIZE
                pygame.draw.rect(self.screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)

                # Dessiner les pions
                piece = self.board[row][col]
                if piece == 'X':
                    pygame.draw.circle(
                        self.screen, BLACK,
                        (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        CELL_SIZE // 3
                    )
                elif piece == 'O':
                    pygame.draw.circle(
                        self.screen, WHITE,
                        (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        CELL_SIZE // 3
                    )
                    pygame.draw.circle(
                        self.screen, BLACK,
                        (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        CELL_SIZE // 3, 2
                    )

        # Si un pion est sélectionné, mettre en évidence
        if self.selected_piece:
            row, col = self.selected_piece
            x, y = MARGIN + col * CELL_SIZE, 100 + row * CELL_SIZE
            pygame.draw.rect(self.screen, RED, (x, y, CELL_SIZE, CELL_SIZE), 3)

        pygame.display.flip()

    def get_cell_from_mouse(self, pos):
        """Retourne la cellule cliquée en fonction de la position de la souris."""
        x, y = pos

        # Soustraire la marge horizontale pour la position de la grille
        x -= MARGIN

        # Soustraire la position de l'interface en haut (100) pour les cellules
        y -= 100

        # Calculer les indices de la cellule
        row, col = y // CELL_SIZE, x // CELL_SIZE

        # Vérifier que les indices sont valides pour la grille
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return row, col
        return None

    def handle_click(self, pos):
        """Gère les clics de souris."""
        if self.popup_active:
            return  # Ne rien faire si la popup est active

        cell = self.get_cell_from_mouse(pos)
        if cell:
            row, col = cell

            # Vérifiez si un pion est sélectionné
            if self.turn_count < 8:
                # Placer un nouveau pion si c'est encore la phase de placement
                self.place_piece(row, col)
            else:
                # Phase de déplacement des pions
                player_symbol = self.player_symbols[self.current_player]

                if self.selected_piece:
                    # Si un autre pion est cliqué et appartient au joueur actuel, changez de sélection
                    if self.board[row][col] == player_symbol:
                        self.select_piece(row, col)
                    else:
                        # Déplacez le pion sélectionné
                        self.move_piece(self.selected_piece, row, col)
                else:
                    # Si aucun pion n'est sélectionné, sélectionnez ce pion
                    if self.board[row][col] == player_symbol:
                        self.select_piece(row, col)

    def place_piece(self, row, col):
        """Place un pion."""
        if self.board[row][col] == ' ':
            player_symbol = self.player_symbols[self.current_player]
            self.board[row][col] = player_symbol
            self.player_pieces[player_symbol].append((row, col))
            self.turn_count += 1

            if check_victory(self.board, player_symbol):
                self.show_popup(f"Le joueur {self.current_player + 1} ({player_symbol}) a gagné!")

            self.switch_player()
        else:
            print("Case occupée.")

    def select_piece(self, row, col):
        """Sélectionne un pion."""
        player_symbol = self.player_symbols[self.current_player]
        if (row, col) in self.player_pieces[player_symbol]:
            self.selected_piece = (row, col)

    def move_piece(self, piece, row, col):
        """Déplace un pion."""
        old_row, old_col = piece
        if self.board[row][col] == ' ' and self.is_adjacent(piece, (row, col)):
            player_symbol = self.player_symbols[self.current_player]

            # Calculer les positions en pixels
            start_x, start_y = MARGIN + old_col * CELL_SIZE, 100 + old_row * CELL_SIZE
            end_x, end_y = MARGIN + col * CELL_SIZE, 100 + row * CELL_SIZE

            # Vider l'ancienne case avant l'animation
            self.board[old_row][old_col] = ' '
            self.redraw_board()

            # Effectuer l'animation
            self.animate_piece((start_x, start_y), (end_x, end_y), player_symbol)

            # Remplir la nouvelle case après l'animation
            self.board[row][col] = player_symbol
            self.redraw_board()

            # Mettre à jour les données du joueur
            self.player_pieces[player_symbol].remove((old_row, old_col))
            self.player_pieces[player_symbol].append((row, col))
            self.selected_piece = None

            # Vérifier la victoire
            if check_victory(self.board, player_symbol):
                self.show_popup(f"Le joueur {self.current_player + 1} ({player_symbol}) a gagné!")

            # Changer de joueur
            self.switch_player()
        else:
            print("Déplacement invalide ou non adjacent.")

    def is_adjacent(self, piece, target):
        """Vérifie si la case cible est adjacente au pion sélectionné."""
        old_row, old_col = piece
        row, col = target
        return abs(old_row - row) <= 1 and abs(old_col - col) <= 1

    def switch_player(self):
        """Change le joueur actuel."""
        self.current_player = 1 - self.current_player

    # Fonction pour afficher la popup
    def show_popup(self, message):
        """Affiche une fenêtre contextuelle avec un message."""
        self.popup_active = True  # Activer la popup
        popup_width = 400
        popup_height = 200
        popup_x = (WINDOW_WIDTH - popup_width) // 2
        popup_y = (WINDOW_HEIGHT - popup_height) // 2

        pygame.draw.rect(self.screen, WHITE, (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(self.screen, BLACK, (popup_x, popup_y, popup_width, popup_height), 3)

        text_surface = self.font.render(message, True, BLACK)
        self.screen.blit(text_surface, (popup_x + (popup_width - text_surface.get_width()) // 2, popup_y + 50))

        # Dessiner les boutons
        quit_button = pygame.Rect(popup_x + 50, popup_y + 120, 150, 40)
        menu_button = pygame.Rect(popup_x + 250, popup_y + 120, 120, 40)
        pygame.draw.rect(self.screen, RED, quit_button)
        pygame.draw.rect(self.screen, BLUE, menu_button)

        quit_text = self.font.render("Quitter", True, WHITE)
        menu_text = self.font.render("Menu", True, WHITE)
        self.screen.blit(quit_text, (quit_button.x + 10, quit_button.y + 5))
        self.screen.blit(menu_text, (menu_button.x + 10, menu_button.y + 5))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    elif menu_button.collidepoint(event.pos):
                        waiting = False
                        pygame.time.delay(1000)
                        self.launch_main()  # Appel de la fonction pour revenir au menu

        self.popup_active = False  # Désactiver la popup

    # Nouvelle fonction pour revenir au menu
    def launch_main(self):
        """Lance le menu principal."""
        try:
            # Lancer le menu
            menu = TeekoMenu()
            mode, difficulty = menu.run_menu()

            print(f"Mode sélectionné : {mode}, Difficulté : {difficulty}")

            # Assurez-vous que l'écran du menu est fermé avant de démarrer le jeu
            pygame.display.quit()

            # Lancer le jeu selon le mode sélectionné
            if mode == "PvP":
                game = TeekoGamePygame(mode)
            elif mode == "PvAI":
                game = TeekoGamePygame(mode, difficulty)

            game.run_game()
        except Exception as e:
            print(f"Une erreur est survenue : {e}")
        finally:
            # Quittez Pygame proprement
            pygame.quit()
            sys.exit()

    def run_game(self):
        """Boucle principale du jeu."""
        running = True
        while running:
            self.draw_board()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            # Si c'est au tour de l'IA, faire jouer l'IA
            if self.mode == "PvAI" and self.current_player == 1:
                self.ai_turn()

        # Ajouter la popup à la fin de la boucle du jeu
        self.show_popup("Test")
        pygame.quit()


    def ai_turn(self):
        """Exécute le tour de l'IA."""
        print("C'est au tour de l'IA...")
        player_symbol = 'O'

        # Vérifiez si le mode est 'hard', 'medium' ou 'easy'
        if self.difficulty == "Difficile":
            print("Mode hard")
            if self.turn_count < 8:
                row, col = ai_alphabeta(self.board, player_symbol,turn_count=self.turn_count)
                self.place_piece(row, col)
            else:
                move = ai_alphabeta(self.board, player_symbol,turn_count=self.turn_count)
                if move and self.board[move[0][0]][move[0][1]] == player_symbol:
                    self.move_piece(move[0], move[1][0], move[1][1])
                else:
                    print("Aucun déplacement possible pour l'IA.")
        elif self.difficulty == "Moyen":
            print("Mode moyen")
            # Appel à la future IA moyen
            if self.turn_count < 8:
                row, col = ai_minmax(self.board, player_symbol, self.turn_count)
                self.place_piece(row, col)
            else:
                move = ai_minmax(self.board, player_symbol, self.turn_count)
                if move and self.board[move[0][0]][move[0][1]] == player_symbol:
                    self.move_piece(move[0], move[1][0], move[1][1])
                else:
                    print("Aucun déplacement possible pour l'IA.")
        else:
            print("Mode easy")
            if self.turn_count < 8:
                row, col = ai_greedy(self.board, player_symbol,turn_count=self.turn_count)
                self.place_piece(row, col)
            else:
                move = ai_greedy(self.board, player_symbol, turn_count=self.turn_count)
                if move and self.board[move[0][0]][move[0][1]] == player_symbol:
                    self.move_piece(move[0], move[1][0], move[1][1])
                print("Aucun déplacement possible pour l'IA.")

    def animate_piece(self, start_pos, end_pos, player_symbol):
        """Anime le déplacement d'un pion entre deux positions."""
        start_x, start_y = start_pos
        end_x, end_y = end_pos

        # Créer une copie de l'écran pour éviter les artefacts
        board_snapshot = self.screen.copy()

        # Déterminer la couleur et la forme du pion
        color = BLACK if player_symbol == 'X' else WHITE
        border_color = None if player_symbol == 'X' else BLACK

        # Effacer le pion de départ en redessinant la case
        pygame.draw.rect(
            self.screen,
            BACKGROUND_COLOR,  # Assurez-vous que cette couleur correspond à la couleur de fond de la grille
            (start_x, start_y, CELL_SIZE, CELL_SIZE)
        )

        # Mettre à jour l'affichage pour que la case de départ soit immédiatement vide
        pygame.display.flip()

        # Fractionner le mouvement en étapes pour lisser l'animation
        steps = 20
        for step in range(steps + 1):
            # Calculer la position intermédiaire
            current_x = start_x + (end_x - start_x) * step / steps
            current_y = start_y + (end_y - start_y) * step / steps

            # Dessiner le fond de la grille à partir de la copie
            self.screen.blit(board_snapshot, (0, 0))

            # Dessiner le pion à la position intermédiaire
            pygame.draw.circle(
                self.screen, color,
                (int(current_x + CELL_SIZE // 2), int(current_y + CELL_SIZE // 2)),
                CELL_SIZE // 3
            )
            if border_color:
                pygame.draw.circle(
                    self.screen, border_color,
                    (int(current_x + CELL_SIZE // 2), int(current_y + CELL_SIZE // 2)),
                    CELL_SIZE // 3, 2
                )

            # Mettre à jour l'affichage
            pygame.display.flip()

            # Ajouter un léger délai pour rendre l'animation visible
            pygame.time.delay(30)

    def redraw_board(self):
        """Redessine uniquement les pions qui changent sans affecter le fond."""
        """Redessine uniquement les pions qui changent sans affecter le fond."""
        if not hasattr(self, 'previous_board'):
            # Initialisez le plateau précédent avec l'état actuel du plateau
            self.previous_board = [row[:] for row in self.board]

        for r, row in enumerate(self.board):
            for c, cell in enumerate(row):
                if self.previous_board[r][c] != cell:
                    # Effacer l'ancien pion (remet le fond intact) uniquement si un changement est détecté
                    pygame.draw.rect(
                        self.screen,
                        WHITE,  # Fond de la case
                        (MARGIN + c * CELL_SIZE, 100 + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )
                    # Redessiner la grille pour garder l'aspect des lignes
                    pygame.draw.rect(
                        self.screen,
                        BACKGROUND_COLOR,
                        (MARGIN + c * CELL_SIZE, 100 + r * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                        1  # Épaisseur de la ligne de grille
                    )

                    # Dessiner le pion à la nouvelle position, si la case n'est pas vide
                    if cell != ' ':
                        color = BLACK if cell == 'X' else WHITE
                        border_color = None if cell == 'X' else BLACK
                        pygame.draw.circle(
                            self.screen, color,
                            (MARGIN + c * CELL_SIZE + CELL_SIZE // 2, 100 + r * CELL_SIZE + CELL_SIZE // 2),
                            CELL_SIZE // 3
                        )
                        if border_color:
                            pygame.draw.circle(
                                self.screen, border_color,
                                (MARGIN + c * CELL_SIZE + CELL_SIZE // 2, 100 + r * CELL_SIZE + CELL_SIZE // 2),
                                CELL_SIZE // 3, 2
                            )

        # Mettre à jour l'état précédent pour comparer lors du prochain appel
        self.previous_board = [row[:] for row in self.board]

        # Mettre à jour l'affichage
        pygame.display.flip()
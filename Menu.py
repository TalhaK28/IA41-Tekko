import pygame
import sys

# Paramètres de l'écran
SCREEN_RATIO = (16, 9)
SCREEN_WIDTH = 1280  # Largeur par défaut pour une résolution 16:9
SCREEN_HEIGHT = int(SCREEN_WIDTH / SCREEN_RATIO[0] * SCREEN_RATIO[1])
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
LIGHT_GRAY = (100, 100, 100)
BLUE = (70, 130, 180)
HOVER_BLUE = (100, 160, 210)

class TeekoMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Teeko Menu")
        self.font_title = pygame.font.Font(None, 72)
        self.font_button = pygame.font.Font(None, 48)
        self.running = True
        self.mode = None
        self.difficulty = None

    def draw_menu(self):
        """Dessine le menu avec les options disponibles."""
        self.screen.fill(GRAY)

        # Titre du menu
        title_text = self.font_title.render("Teeko: Choisissez un mode", True, WHITE)
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        # Boutons
        self.draw_button("Joueur vs Joueur", SCREEN_WIDTH // 2 - 200, 300, 400, 60, "PvP")
        self.draw_button("Joueur vs IA (Facile)", SCREEN_WIDTH // 2 - 200, 400, 400, 60, "AI_Easy")
        self.draw_button("Joueur vs IA (Difficile)", SCREEN_WIDTH // 2 - 200, 500, 400, 60, "AI_Hard")

        pygame.display.flip()

    def draw_button(self, text, x, y, width, height, action):
        """Dessine un bouton avec un effet d'ombre et gère les clics."""
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Vérifier le survol
        is_hovered = x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height
        color = HOVER_BLUE if is_hovered else BLUE

        # Dessiner l'ombre
        pygame.draw.rect(self.screen, LIGHT_GRAY, (x + 5, y + 5, width, height))

        # Dessiner le bouton
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        pygame.draw.rect(self.screen, WHITE, (x, y, width, height), 2)

        # Ajouter le texte
        text_surface = self.font_button.render(text, True, WHITE)
        self.screen.blit(text_surface, (x + width // 2 - text_surface.get_width() // 2, y + height // 2 - text_surface.get_height() // 2))

        # Vérifier si le bouton est cliqué
        if click[0] == 1 and is_hovered:
            pygame.time.delay(300)  # Pause pour éviter des clics multiples
            if action == "PvP":
                self.mode = "PvP"
                self.running = False
            elif action == "AI_Easy":
                self.mode = "PvAI"
                self.difficulty = "Facile"
                self.running = False
            elif action == "AI_Hard":
                self.mode = "PvAI"
                self.difficulty = "Difficile"
                self.running = False

    def run_menu(self):
        """Boucle principale du menu."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self.draw_menu()

        return self.mode, self.difficulty

if __name__ == "__main__":
    menu = TeekoMenu()
    mode, difficulty = menu.run()
    print(f"Mode choisi: {mode}, Difficulté: {difficulty}")
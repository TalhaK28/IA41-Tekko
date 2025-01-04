from Menu import TeekoMenu
from Jeu import TeekoGamePygame
import pygame
import sys

# Lancer le menu
if __name__ == "__main__":
    pygame.init()

    try:
        # Lancer le menu
        menu = TeekoMenu()
        mode, difficulty = menu.run_menu()

        print(f"Mode choisi: {mode}, Difficulté: {difficulty}")

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
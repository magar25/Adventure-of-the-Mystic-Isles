import pygame
import sys
from settings import *
from level import Level


class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Adventure of the Mystic Isles')
        self.clock = pygame.time.Clock()

        self.level = Level()

        # sound
        self.main_sound = pygame.mixer.Sound('../audio/main.ogg')
        self.main_sound.set_volume(0.1)
        self.main_sound.play(loops=-1)

        # Game over screen setup
        self.game_over_font = pygame.font.Font(None, 80)  # Larger font size (72)
        self.game_over_text = self.game_over_font.render("Game Over", True, (255, 255, 255))

        # Font for "Restart" and "Quit" text
        self.restart_font = pygame.font.Font(None, 40)
        self.quit_font = pygame.font.Font(None, 40)

        # Render "Restart" and "Quit" text
        self.restart_text = self.restart_font.render("Press SPACE to Restart", True, (255, 255, 255))
        self.quit_text = self.quit_font.render("Press ESC to Quit the Game", True, (255, 255, 255))

        # Calculate positions for the text
        text_height = self.game_over_text.get_height()
        restart_height = self.restart_text.get_height()
        quit_height = self.quit_text.get_height()

        y_position = (HEIGHT - (text_height + restart_height + quit_height)) // 2

        self.game_over_screen = pygame.Surface((WIDTH, HEIGHT))
        self.game_over_screen.fill((0, 0, 0))
        self.game_over_screen.blit(self.game_over_text, (WIDTH // 2 - 180, y_position))
        y_position += text_height
        self.game_over_screen.blit(self.restart_text, (WIDTH // 2 - 180, y_position))
        y_position += restart_height
        self.game_over_screen.blit(self.quit_text, (WIDTH // 2 - 180, y_position))

        self.game_over = False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.level.toggle_menu()

            if not self.game_over:
                self.screen.fill(WATER_COLOR)
                self.level.run()
                pygame.display.update()
                self.clock.tick(FPS)

                # Check player's HP and set game over flag if it's <= 0
                if self.level.player.health <= 0:
                    self.game_over = True
                    self.main_sound.set_volume(0)  # Pause the main sound

            # Display game over screen and handle input to restart or quit
            else:
                self.screen.blit(self.game_over_screen, (0, 0))
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            # Reset the game when 'SPACE' is pressed
                            self.level = Level()
                            self.game_over = False
                            self.main_sound.set_volume(0.1)
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()

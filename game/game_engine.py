import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.large_font = pygame.font.SysFont("Arial", 60)

        self.game_over = False
        self.winner = None

        # 🎵 Load sounds
        try:
            self.sounds = {
                "paddle": pygame.mixer.Sound("game/sounds/paddle_hit.wav"),
                "wall": pygame.mixer.Sound("game/sounds/wall_bounce.wav"),
                "score": pygame.mixer.Sound("game/sounds/score.wav"),
                "gameover": pygame.mixer.Sound("game/sounds/game_over.wav"),
            }
        except Exception as e:
            print("⚠️ Sound loading error:", e)
            self.sounds = None

    # ------------------ INPUT ------------------
    def handle_input(self):
        keys = pygame.key.get_pressed()

        if not self.game_over:
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)
        else:
            if keys[pygame.K_r]:
                self.reset()
            if keys[pygame.K_ESCAPE]:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # ------------------ UPDATE ------------------
    def update(self):
        if self.game_over:
            return

        # Move ball
        hit_wall = self.ball.move_with_sound(self.sounds)  # <-- modified

        # Check paddle collisions
        hit_paddle = self.ball.check_collision(self.player, self.ai)
        if hit_paddle and self.sounds:
            self.sounds["paddle"].play()

        # Scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            if self.sounds: self.sounds["score"].play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            if self.sounds: self.sounds["score"].play()
            self.ball.reset()

        # Check for win
        if self.player_score >= 5:
            self._end_game("Player")
        elif self.ai_score >= 5:
            self._end_game("AI")

        self.ai.auto_track(self.ball, self.height)

    # ------------------ RENDER ------------------
    def render(self, screen):
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

        if self.game_over:
            msg = f"{self.winner} Wins!"
            msg_text = self.large_font.render(msg, True, WHITE)
            replay_text = self.font.render("Press R to Replay | ESC to Quit", True, WHITE)
            screen.blit(msg_text, (self.width // 2 - msg_text.get_width() // 2, self.height // 2 - 60))
            screen.blit(replay_text, (self.width // 2 - replay_text.get_width() // 2, self.height // 2 + 20))

    def _end_game(self, winner):
        self.game_over = True
        self.winner = winner
        if self.sounds:
            self.sounds["gameover"].play()

    def reset(self):
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.player.y = self.height // 2 - self.paddle_height // 2
        self.ai.y = self.height // 2 - self.paddle_height // 2
        self.game_over = False
        self.winner = None

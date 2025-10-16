import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    # def move(self):
    #     self.x += self.velocity_x
    #     self.y += self.velocity_y

    #     if self.y <= 0 or self.y + self.height >= self.screen_height:
    #         self.velocity_y *= -1
    def move_with_sound(self, sounds=None):
        """Move the ball and play wall sound if bounced."""
        self.x += self.velocity_x
        self.y += self.velocity_y
        hit_wall = False

        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            hit_wall = True
            if sounds:
                sounds["wall"].play()

        return hit_wall


    # def check_collision(self, player, ai):
    #     if self.rect().colliderect(player.rect()) or self.rect().colliderect(ai.rect()):
    #         self.velocity_x *= -1

    # def check_collision(self, player, ai):
    #     ball_rect = self.rect()

    #     # Player paddle collision (left)
    #     if ball_rect.colliderect(player.rect()):
    #         self.x = player.x + player.width  # push ball outside paddle
    #         self.velocity_x = abs(self.velocity_x)  # ensure moving right

    #         # Adjust Y velocity based on where it hit on the paddle
    #         offset = (self.y + self.height / 2) - (player.y + player.height / 2)
    #         self.velocity_y = offset * 0.1  # tweak factor for bounce angle

    #     # AI paddle collision (right)
    #     elif ball_rect.colliderect(ai.rect()):
    #         self.x = ai.x - self.width  # push ball outside paddle
    #         self.velocity_x = -abs(self.velocity_x)  # ensure moving left

    #         offset = (self.y + self.height / 2) - (ai.y + ai.height / 2)
    #         self.velocity_y = offset * 0.1  # tweak factor for bounce angle

    #     # Optional: Slight speed increase every hit for challenge
    #     self.velocity_x *= 1.0
    #     self.velocity_y *= 1.0

    def check_collision(self, player, ai):
        ball_rect = self.rect()
        collided = False

        if ball_rect.colliderect(player.rect()):
            self.x = player.x + player.width
            self.velocity_x = abs(self.velocity_x)
            offset = (self.y + self.height / 2) - (player.y + player.height / 2)
            self.velocity_y = offset * 0.1
            collided = True

        elif ball_rect.colliderect(ai.rect()):
            self.x = ai.x - self.width
            self.velocity_x = -abs(self.velocity_x)
            offset = (self.y + self.height / 2) - (ai.y + ai.height / 2)
            self.velocity_y = offset * 0.1
            collided = True

        if collided:
            self.velocity_x *= 1.05
            self.velocity_y *= 1.05

        return collided



    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

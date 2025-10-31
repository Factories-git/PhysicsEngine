import numpy, math

import pygame
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
elasticity = -0.85  # 탄성, 20% 손실 발생, 80% 유지
friction = 0.995  # 마찰 계수 (숫자가 낮으면 마찰력 상승)
gravity = pygame.math.Vector2(0, 0.5)
ball_number = 1


class Ball:
    def __init__(self, x, y, radius=0, color=()):
        global ball_number
        self.ball_number = ball_number
        ball_number += 1
        self.position = pygame.math.Vector2(x, y)
        if radius <= 0:
            radius = random.randrange(10, 30)
        self.velocity = pygame.math.Vector2(random.uniform(-5, 5), 5)
        self.prev_velocity = None
        self.radius = radius
        self.mass = radius ** 2  # 질량

        if not color:
            color = (random.randrange(256), random.randrange(256), random.randrange(256))
        self.color = color

    def update(self, nx=SCREEN_WIDTH, ny=SCREEN_HEIGHT):
        if self.prev_velocity is None:
            self.prev_velocity = pygame.math.Vector2(0, 0)
            self.prev_velocity.x = numpy.ceil((self.velocity.x*100)/100)
            self.prev_velocity.y = numpy.ceil((self.velocity.y*100)/100)
        self.velocity += gravity # 중력
        self.velocity *= friction  # 마찰력 작용
        if abs(self.velocity.x) < 1:
            self.velocity.x = 0
        self.velocity.y = numpy.ceil((self.velocity.y*100)/100)
        self.velocity.x = numpy.ceil((self.velocity.x*100)/100)

        if round(self.prev_velocity.y) == round(self.velocity.y):
            self.velocity.y = self.prev_velocity.y = 0
        else:
            self.prev_velocity.y = numpy.ceil((self.velocity.y*100)/100)
        self.position += self.velocity
        if self.position.x + self.radius >= nx:
            self.position.x = nx - self.radius
            self.velocity.x *= elasticity
        if self.position.x - self.radius <= 0:
            self.position.x = self.radius
            self.velocity.x *= elasticity
        if self.position.y + self.radius >= ny:
            self.position.y = ny - self.radius
            self.velocity.y *= elasticity
        if self.position.y - self.radius <= 0:
            self.position.y = self.radius
            self.velocity.y *= elasticity

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (
            int(self.position.x), int(self.position.y)
        ), self.radius)

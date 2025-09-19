import pygame, random

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
elasticity = -0.85  # 탄성, 20% 손실 발생, 80% 유지
friction = 0.997  # 마찰 계수 (숫자가 낮으면 마찰력 상승)
gravity = pygame.math.Vector2(0, 0.5)


class Ball:
    def __init__(self, x, y, radius=0, color=()):
        self.position = pygame.math.Vector2(x, y)
        if radius <= 0:
            radius = random.randrange(10, 30)
        self.radius = radius
        if not color:
            color = (random.randrange(256), random.randrange(256), random.randrange(256))
        self.color = color
        self.velocity = pygame.math.Vector2(random.uniform(-5, 5), random.uniform(-5, 5))

    def update(self, nx=SCREEN_WIDTH, ny=SCREEN_HEIGHT):
        self.velocity += gravity
        self.velocity *= friction  # 마찰력 작용
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

    def collision_check(self, other):
        d = self.position - other.position
        if d.length() <= self.radius + other.radius:
            return True
        return False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (
            int(self.position.x), int(self.position.y)
        ), self.radius)

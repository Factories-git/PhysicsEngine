
from ball import Ball
import pygame


pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("STEP 4 : 공 튕기기")
clock = pygame.time.Clock()

is_run = True

black = (0, 0, 0)
# 공에 관련된 변수들

# 중력 가속도
gravity = pygame.math.Vector2(0, 0.5)
elasticity = -0.85 # 탄성, 20% 손실 발생, 80% 유지


balls = []

while is_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            ball = Ball(x, y)
            balls.append(ball)
    for i in range(len(balls)):
        for j in range(i+1, len(balls)):
            distance_vector = balls[i].position - balls[j].position
            if distance_vector.length_squared() == 0:
                continue
            distance = distance_vector.length()
            if distance <= balls[i].radius + balls[j].radius:
                overlap = (balls[i].radius + balls[j].radius) - distance
                push_vector = distance_vector.normalize() * overlap
                balls[i].position += push_vector / 2
                balls[j].position -= push_vector / 2
                balls[i].velocity, balls[j].velocity = balls[j].velocity, balls[i].velocity

    for ball in balls:
        ball.update(gravity)
    # 배경
    screen.fill(black)
    # 공 그리기
    for i in range(len(balls)):
        balls[i].draw(screen)

    pygame.display.flip()
    clock.tick(70)
pygame.quit()
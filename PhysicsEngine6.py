from ball import Ball
import pygame

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("STEP 6 : '질량'은 부피와 비례하지 않는다.")
clock = pygame.time.Clock()

is_run = True

black = (0, 0, 0)

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
        for j in range(i + 1, len(balls)):
            distance_vector = balls[i].position - balls[j].position
            if distance_vector.length_squared() == 0:
                continue
            distance = distance_vector.length()
            normal_vector = distance_vector.normalize()
            if distance <= balls[i].radius + balls[j].radius:
                overlap = (balls[i].radius + balls[j].radius) - distance
                push_vector = normal_vector * overlap
                balls[i].position += push_vector / 2
                balls[j].position -= push_vector / 2
                # 질량 -> 충돌 반응 개선 (2D 탄성 충돌 공식 적용), 질량 고려
                tangent_vector = pygame.math.Vector2(-normal_vector.y, normal_vector.x)

                v1n = balls[i].velocity.dot(normal_vector)
                v2n = balls[j].velocity.dot(normal_vector)
                v1t = balls[i].velocity.dot(tangent_vector)
                v2t = balls[j].velocity.dot(tangent_vector)

                m1, m2 = balls[i].mass, balls[j].mass
                new_v1n = (v1n * (m1 - m2) + 2 * m2 * v2n) / (m1 + m2)
                new_v2n = (v2n * (m2 - m1) + 2 * m1 * v1n) / (m1 + m2)

                balls[i].velocity = (normal_vector * new_v1n) + (tangent_vector * v1t)
                balls[j].velocity = (normal_vector * new_v2n) + (tangent_vector * v2t)

    for ball in balls:
        ball.update()
    # 배경
    screen.fill(black)
    # 공 그리기
    for i in range(len(balls)):
        balls[i].draw(screen)

    pygame.display.flip()
    clock.tick(70)
pygame.quit()

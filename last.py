import pygame
import pymunk
import random

pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("pymunk 물리엔진")
clock = pygame.time.Clock()

background_color = (0, 0, 0)
is_run = True

# pymunk 초기화
space = pymunk.Space()  # 물리 공간
# 중력
space.gravity = (0, 900)
# 정적(static) 경계선 (벽) Segment(몸체, 시작점, 끝점, 두께)
floor = pymunk.Segment(space.static_body, (0, screen_height - 10), (screen_width, screen_height - 10), 5)
floor.elasticity = 0.85
floor.friction = 1.0
left_wall = pymunk.Segment(space.static_body, (0, 0), (0, screen_height), 5)
right_wall = pymunk.Segment(space.static_body, (screen_width, 0), (screen_width, screen_height), 5)
top_wall = pymunk.Segment(space.static_body, (0, 0), (screen_width, 0), 5)
space.add(floor)
space.add(left_wall, right_wall, top_wall)

balls = []


def create_ball(x, y):
    radius = random.randint(10, 30)
    mass = radius ** 2 * 3.1415926535897932387263
    # Body(질량, 관성 정보(질량, 속도, radius)), 물리적 속성임
    body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))
    body.position = (x, y)
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.6  # 공 탄성
    shape.friction = 0.8

    space.add(body, shape)
    color = (random.randrange(256), random.randrange(256), random.randrange(256))
    balls.append((shape, color))


while is_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            create_ball(x, y)

    # event 처리
    dt = 1 / 60
    space.step(dt)

    #draw
    screen.fill(background_color)
    for ball_shape, ball_color in balls:
        x = ball_shape.body.position.x
        y = ball_shape.body.position.y
        radius = ball_shape.radius
        pygame.draw.circle(screen, ball_color, (x, y), radius)

    pygame.draw.line(screen, (255, 255, 255), (0, screen_height-10), (screen_width, screen_height-10), 10)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

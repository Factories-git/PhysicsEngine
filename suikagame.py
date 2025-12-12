import pygame
import pymunk
import random
import constant

pygame.init()

screen = pygame.display.set_mode((constant.screen_width, constant.screen_height))
pygame.display.set_caption(constant.game_title)
clock = pygame.time.Clock()

# pymunk 초기화
space = pymunk.Space()  # 물리 공간
# 중력
space.gravity = (0, 900)
collision_type = 1


def create_wall(p1, p2):  #p1: 시작점, p2: 끝 지점
    wall = pymunk.Segment(space.static_body, p1, p2, 10)
    wall.elasticity = constant.elasticity
    wall.friction = constant.friction
    space.add(wall)


fruits = []  # 과일 리스트
ball_types = constant.ball_types


def create_fruit(x, y, level):  # level: index
    if level < 0 or level >= len(ball_types):
        return
    radius, color = ball_types[level]

    body = pymunk.Body(level+1, pymunk.moment_for_circle(level+1, 0, radius))
    body.position = (x, y)
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.3
    shape.friction = 0.5
    shape.collision_type = collision_type
    shape.level = level # 모양 정보
    shape.color = color
    shape.is_removed = False # 삭제 되어져야 할 공에 대한 상태 정보

    space.add(body, shape)
    fruits.append(shape)


def resolve_collision(space, f1, f2):
    if f1.is_removed or f2.is_removed:
        return
    f1.is_removed = True
    f2.is_removed = True
    space.remove(f1.body, f1)
    space.remove(f2.body, f2)
    if f1 in fruits:
        fruits.remove(f1)
    if f2 in fruits:
        fruits.remove(f2)
    new_x = (f1.body.position.x + f2.body.position.x) / 2
    new_y = (f1.body.position.y + f1.body.position.y) / 2
    create_fruit(new_x, new_y, f1.level + 1)


def collision_start(arbiter, space, data):
    f1, f2 = arbiter.shapes
    if f1.level == f2.level:
        space.add_post_step_callback(resolve_collision, f1, f2)
        return False # 충돌 안됐니? -> 응 됨
    return True # -> ㄴㄴ 아님


handler = space.add_collision_handler(collision_type, collision_type)
handler.begin = collision_start
is_run = True
current_fruit = 0
height = constant.screen_height
width = constant.screen_width
create_wall((0, height), (width, height)) #아래
create_wall((0,0), (0, height)) #좌
create_wall((width, 0), (width, height))

while is_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            create_fruit(event.pos[0], 50, current_fruit)
            current_fruit = random.randint(0, 3)
    space.step(1 / constant.fps)
    screen.fill(constant.background_color)

    for fruit in fruits:
        pos = tuple(map(int, fruit.body.position))
        pygame.draw.circle(screen, fruit.color, pos, int(fruit.radius))

    pygame.display.flip()
    clock.tick(constant.fps)


pygame.quit()

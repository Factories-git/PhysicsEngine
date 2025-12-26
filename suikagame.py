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
wall_lines = []

def create_wall(p1, p2):  #p1: 시작점, p2: 끝 지점
    wall = pymunk.Segment(space.static_body, p1, p2, 5)
    wall.elasticity = constant.elasticity
    wall.friction = constant.friction
    space.add(wall)
    wall_lines.append((p1, p2))


fruits = []  # 과일 리스트
ball_types = constant.ball_types


def create_fruit(x, y, level):  # level: index
    if level < 0 or level >= len(ball_types):
        return
    radius, color = ball_types[level]
    mass = level + 1
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)

    body.position = (x, y)
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.3
    shape.friction = 0.5
    shape.collision_type = collision_type
    shape.level = level # 모양 정보
    shape.color = color
    shape.is_removed = False # 삭제 되어져야 할 공에 대한 상태 정보
    shape.spawn_time = pygame.time.get_ticks()

    space.add(body, shape)
    fruits.append(shape)


def resolve_collision(space, f1, f2):
    global score
    if f1.is_removed or f2.is_removed:
        return
    if f1.level == len(ball_types) - 1 == f2.level:
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
    score += (f1.level+1) * 10


def collision_start(arbiter, space, data):
    f1, f2 = arbiter.shapes
    if f1.level == f2.level:
        if f1.level == len(ball_types) - 1:
            return True
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
deadline_y = 150
is_game_over = False
score = 0


while is_run:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not is_game_over and event.button == 1:
            mouse_x = event.pos[0]
            radius = ball_types[current_fruit][0]
            use_x = max(radius, min(width-radius, mouse_x))
            create_fruit(use_x, 50, current_fruit)
            current_fruit = random.randint(0, 3)
    if not is_game_over:
        space.step(1 / constant.fps)
        screen.fill(constant.background_color)

    for p1, p2 in wall_lines:
        pygame.draw.line(screen, constant.wall_color, p1, p2, 5)

    pygame.draw.line(screen, constant.deadline_color, (0, deadline_y), (width, deadline_y), 2)
    for fruit in fruits:
        pos = tuple(map(int, fruit.body.position))
        pygame.draw.circle(screen, fruit.color, pos, int(fruit.radius))
        if (pos[1] < deadline_y - fruit.radius) and current_time - fruit.spawn_time > 1000:
            is_game_over = True

    if not is_game_over:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        r_preview = ball_types[current_fruit][0] #반지름
        c_preview = ball_types[current_fruit][1] #색상

        preview_x = max(r_preview, min(width-r_preview, mouse_x))
        pygame.draw.circle(screen, c_preview, (preview_x, 50), r_preview)
        pygame.draw.line(screen, (180, 180, 180), (preview_x, 50), (preview_x, height), 1)

        font = pygame.font.SysFont("Arial", 16, True)
        text = font.render(f"Score : {score}",True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.x = 10
        text_rect.y = 20
        screen.blit(text, text_rect)
    else:
        font = pygame.font.SysFont("Arial", 40, True)
        text = font.render("Game Over!!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(width/2, height/2))
        screen.blit(text, text_rect)
        text = font.render(f"Score : {score}",True, (255, 0, 0))
        text_rect = text.get_rect(center=(width/2, height/2 + 60))
        screen.blit(text, text_rect)
    pygame.display.flip()
    clock.tick(constant.fps)


pygame.quit()

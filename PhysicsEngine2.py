import pygame


pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("STEP 1 : 자유 낙하 운동")
clock = pygame.time.Clock()

is_run = True
white = (255, 255, 255)
black = (0, 0, 0)
# 공에 관련된 변수들
radius = 25
position = pygame.math.Vector2(SCREEN_WIDTH / 2, radius) # 공의 위치
velocity = pygame.math.Vector2(1.25, 0)

# 중력 가속도
gravity = pygame.math.Vector2(0, 0.5)
elasticity = -0.85 # 탄성, 20% 손실 발생, 80% 유지

while is_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_run = False

    # 공식 사용해서 값 바꾸기
    velocity += gravity
    position += velocity

    if position.y + radius >= SCREEN_HEIGHT:
        position.y = SCREEN_HEIGHT - radius
        velocity.y *= elasticity
    # 상좌우 충돌 처리 (homework)
    # 배경
    screen.fill(black)
    # 공 그리기
    pygame.draw.circle(screen, white, (position.x, position.y), radius)

    pygame.display.flip()
    clock.tick(70)
pygame.quit()
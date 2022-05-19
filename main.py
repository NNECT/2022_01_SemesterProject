import sys
from module.class_card import *

pygame.init()

# 초당 프레임 단위 설정
FramePerSec = pygame.time.Clock()

# 게임 창 설정
screen_width = 900  # 가로 크기
screen_height = 600  # 세로 크기
GameDisplay = pygame.display.set_mode((screen_width, screen_height))
GameDisplay.fill(COLOR_BACKGROUND)  # 배경색 채우기
pygame.display.set_caption("Blackjack")  # 창 이름 설정

worklist = []

play1 = Card(HEARTS, ACE, [screen_width // 2, screen_height // 5], opened=False)
play1.set_destination([screen_width // 2, screen_height * 4 // 5])
next_event_time = now() + 1000


while True:
    FramePerSec.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    play1.frame_move()
    GameDisplay.fill(COLOR_BACKGROUND)  # 배경색 채우기

    if can_next_event(next_event_time):
        if not play1.opened:
            play1.flip()
            next_event_time = now() + (1000 * 21 // FPS)


    # 화면 출력
    play1.image_blit(GameDisplay)
    # print(pygame.time.get_ticks())

    pygame.display.update()

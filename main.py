import sys
import pygame
from pygame.locals import *

pygame.init()

# 초당 프레임 단위 설정
FPS = 30
FramePerSec = pygame.time.Clock()

# 컬러 세팅
COLOR_BACKGROUND = (10, 55, 17)

# 게임 창 설정
screen_width = 900  # 가로 크기
screen_height = 600  # 세로 크기
GameDisplay = pygame.display.set_mode((screen_width, screen_height))
GameDisplay.fill(COLOR_BACKGROUND)  # 배경색 채우기
pygame.display.set_caption("Blackjack")  # 창 이름 설정

# 이미지 로딩
# for mark in ['spade', 'heart', 'diamond', 'club']:
#     for number in range(2, 11):
#         filename = f'{number}_of_{mark}s'
#         locals()[f'card_{filename}'] = pygame.image.load(f'images/{filename}.png')
#         locals()[f'card_{filename}_pos'] = [(screen_width - 50) / 2, (screen_height - 72) / 5]  # 화면 가로의 절반 크기에 해당하는 곳에 위치

card_10_of_hearts = pygame.image.load('images/10_of_hearts.png')
card_10_of_hearts_pos = [(screen_width - 50) // 2, (screen_height - 72) // 5]


# 속도 계산
def throw_speed(start_loc: list[int], target_loc: list[int], frame: int, accel: int = 3) -> list[list[int]]:
    # 각 좌표가 양의 방향인지 여부 확인
    is_positive_direction = [start_loc[xy] <= target_loc[xy] for xy in range(2)]
    # 각 좌표의 이동 거리의 절댓값을 구함
    displace = [(target_loc[xy] - start_loc[xy]) if is_pd else (target_loc[xy] - start_loc[xy]) * -1
                for xy, is_pd in enumerate(is_positive_direction)]

    # 속도 구하기
    speed = [[], []]
    for xy in range(2):
        speed[xy].append(displace[xy] // accel)
        for i in range(1, frame - 1):
            speed[xy].append(speed[xy][i - 1] * (accel - 1) // accel)
        speed[xy].append(displace[xy] - sum(speed[xy]))
        speed[xy].sort(reverse=True)

    # [x, y] 리스트 형태로 반환
    return [[moment[0], moment[1]] for moment in zip(*speed)]


move_speed = throw_speed(card_10_of_hearts_pos, [card_10_of_hearts_pos[0], card_10_of_hearts_pos[1] * 4], FPS * 2)
wait_time = 60
moving_time = len(move_speed)

while True:
    FramePerSec.tick(FPS)

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if wait_time > 0:
        wait_time -= 1
    else:
        if len(move_speed) > 0:
            temp = move_speed[0]
            for xy in range(2):
                card_10_of_hearts_pos[xy] += int(temp[xy])
            move_speed.remove(temp)
            GameDisplay.fill(COLOR_BACKGROUND)  # 배경색 채우기

    # 화면 출력
    GameDisplay.blit(card_10_of_hearts, (card_10_of_hearts_pos[0], card_10_of_hearts_pos[1]))

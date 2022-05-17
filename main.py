import sys
import pygame
from pygame.locals import *

## pygame 기능 사용을 시작하는 명령어 ##
pygame.init()

## 초당 프레임 단위 설정 ##
FPS = 30
FramePerSec = pygame.time.Clock()

## 컬러 세팅 ##
COLOR_BACKGROUND = (10, 55, 17)

## 게임 창 설정 ##
GameDisplay = pygame.display.set_mode((900,600))
GameDisplay.fill(COLOR_BACKGROUND) #배경색 채우기
pygame.display.set_caption("Blackjack") #창 이름 설정

while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    FramePerSec.tick(FPS)

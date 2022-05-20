import pygame
from pygame.locals import *
from typing import Final

# 게임 기초 세팅

screen_width: Final = 900  # 가로 크기
screen_height: Final = 600  # 세로 크기
FPS: Final = 30  # 화면 초당 프레임
COLOR_BACKGROUND: Final = (10, 55, 17)  # 화면 배경색
CARD_SIZE: Final = [50, 72]
DECK_LOCATION: Final = [600, 100]

def now() -> int:
    return pygame.time.get_ticks()

def can_next_event(next_event_time) -> bool:
    return pygame.time.get_ticks() > next_event_time
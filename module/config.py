import sys, random, time, pygame
from pygame.locals import *

from typing import Final, Any, Optional


# 카드 상수
SPADE: Final = 1
SPADES: Final = 1
HEART: Final = 2
HEARTS: Final = 2
DIAMOND: Final = 3
DIAMONDS: Final = 3
CLOVER: Final = 4
CLOVERS: Final = 4

ACE: Final = 1
JACK: Final = 11
QUEEN: Final = 12
KING: Final = 13


# 버튼 상수
HIT = 1
STAND = 2
SURRENDER = 3
DOUBLEDOWN = 4
INSURANCE = 5
SPLIT = 6
EVENMONEY = 7


# 게임 기초 세팅
screen_width: Final = 900  # 가로 크기
screen_height: Final = 600  # 세로 크기
FPS: Final = 30  # 화면 초당 프레임
COLOR_BACKGROUND: Final = (80, 160, 80)  # (10, 55, 17)  # 화면 배경색
CARD_SIZE: Final = [50, 72]
DECK_LOCATION: Final = [700, 100]
HAND_LOCATION: Final = [[300, 100],
                        [240, 100+72],
                        [360, 100+72]]
BUTTON_SIZE: Final = [140, 30]
BUTTON_LOCATION: Final = [[15 + ((140 + 6) * i), 600 - 45] for i in range(6)]
DEALER_STAND_POINT: Final = 17


import pygame
import threading
import sys
import random
import time
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
HIT: Final = 1
STAND: Final = 2
SURRENDER: Final = 3
DOUBLEDOWN: Final = 4
SPLIT: Final = 5
INSURANCE: Final = 6
EVENMONEY: Final = 7


# 게임 기초 세팅
screen_width: Final = 900  # 가로 크기
screen_height: Final = 600  # 세로 크기
FPS: Final = 30  # 화면 초당 프레임
COLOR_BACKGROUND: Final = (80, 160, 80)  # (10, 55, 17)  # 화면 배경색
CARD_SIZE: Final = [50, 72]
DECK_LOCATION: Final = [700, 100]
CHIPTOWER_LOCATION: Final = [60, 450]
CHIPNUMBER_LOCATION: Final = [70, 470]
HAND_LOCATION: Final = [[350, 120],
                        [250, 340],
                        [500, 340]]
TEXT_LOCATION = [5, -20]
BUTTON_SIZE: Final = [140, 30]
BUTTON_LOCATION: Final = [[40 + (144 + (screen_width - 144 * 5 - 80) // 4) * i, screen_height - 70] for i in range(5)]
DEALER_STAND_POINT: Final = 17
BASE_MONEY = 20
DEAL_MONEY = 2
GAME_OVER_LOCATION = [screen_width // 2 - 267 // 2, screen_height // 2 - 65 // 2]

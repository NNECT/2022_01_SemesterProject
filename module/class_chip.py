# 프로그램 내 모듈
from module.config import *


class Chip:
    chip_image = pygame.image.load('./other_images/chip_on.png')
    chiptower_image = pygame.image.load('./other_images/chip_tower.png')

    @classmethod
    def chip_blit(cls, num: int, display, loc) -> None:
        for i in range(num):
            display.blit(cls.chip_image, (loc[0] + (10 * i), loc[1]))

    @classmethod
    def chiptower_blit(cls, num: int, display) -> None:
        for i in range(num):
            display.blit(cls.chiptower_image, (CHIPTOWER_LOCATION[0], CHIPTOWER_LOCATION[1] - (5 * i)))

# 프로그램 내 모듈
from module.config import *


class Card:
    imagefiles: list[list[Any]] = []
    mark_names: dict = {1: 'spades', 2: 'hearts', 3: 'diamonds', 4: 'clubs'}
    number_names = ['', 'ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'jack', 'queen', 'king']

    def __init__(self, mark: int, number: int, x: int, y: int, opened: bool = True):
        # 이미지 초기화
        if len(self.imagefiles) == 0:
            self.imagefiles = [[pygame.image.load('./card_images/back_of_card.png'), pygame.image.load('./card_images/back_of_card_2.png')]]
            for i in range(1, 4 + 1):
                self.imagefiles.append(
                    [pygame.image.load(f'./card_images/{self.number_names[j]}_of_{self.mark_names[i]}.png')
                     for j in range(1, 13 + 1)])

        # 매개변수 입력
        self.mark: int = mark
        self.number: int = number
        self.loc: list[int] = [x, y]
        self.opened: bool = opened
        self.surface = pygame.Surface(CARD_SIZE)

    def image_blit(self, display: pygame.Surface, deck=False) -> None:
        """이미지 출력"""
        if not deck:
            display.blit(self.imagefile(), self.loc)
        else:
            display.blit(self.imagefiles[0][1], self.loc)

    def imagefile(self) -> pygame.Surface:
        """이미지 파일 참조"""
        if self.opened:
            return self.imagefiles[self.mark][self.number - 1]
        else:
            return self.imagefiles[0][0]

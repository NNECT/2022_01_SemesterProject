# 프로그램 내 모듈
from module.config import *


class Button:
    imagefiles: list[list[Any]] = []
    kinds: dict = {0: 'none', HIT: 'hit', STAND: 'stand', SURRENDER: 'surrender', DOUBLEDOWN: 'doubledown', INSURANCE: 'insurance', SPLIT: 'split', EVENMONEY: 'evenmoney'}
    status: dict = {'off': 0, 'on': 1, 'focus': 2}

    def __init__(self, kind: int, x: int, y: int, on: bool = True):
        # 이미지 초기화
        if len(self.imagefiles) == 0:
            for i in range(8):
                self.imagefiles.append([pygame.image.load(f'./button_images/{self.kinds[i]}({j}).png')
                                        for j in range(3)])

        self.kind = kind
        self.loc = [x, y]
        self.size = BUTTON_SIZE.copy()
        self.is_on = on

    def on_button(self, x: int, y: int):
        if (self.loc[0] < x < self.loc[0] + self.size[0]) and (self.loc[1] < y < self.loc[1] + self.size[1]):
            return True
        else:
            return False

    def image_blit(self, display: pygame.Surface, status: int = None) -> None:
        if self.is_on is False:
            status = 0
        elif status is None:
            status = 1
        if 0 <= status <= 3:
            display.blit(self.imagefile(status), self.loc)

    def imagefile(self, status: int) -> Optional[pygame.Surface]:
        """이미지 파일 참조"""
        if 0 <= status <= 3:
            if 0 < self.kind <= 7:
                return self.imagefiles[self.kind][status]
            else:
                return self.imagefiles[0][0]
        else:
            return

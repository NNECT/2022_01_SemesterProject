from typing import Any, Optional

from module.config import *
from module.variable import *


class Card:
    imagefiles: list[list[Any]] = []
    mark_names: dict = {1: 'spades', 2: 'hearts', 3: 'diamonds', 4: 'clubs'}
    number_names = ['', 'ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'jack', 'queen', 'king']

    def __init__(self, mark: int, number: int, loc: list[int], opened: bool = True):
        # 이미지 초기화
        if len(self.imagefiles) == 0:
            self.imagefiles.append([pygame.image.load('./images/back_of_card.png')])
            for i in range(1, 5):
                self.imagefiles.append(
                    [pygame.image.load(f'./images/{self.number_names[j]}_of_{self.mark_names[i]}.png')
                     for j in range(1, 13 + 1)])

        # 매개변수 입력
        self.mark: int = mark
        self.number: int = number
        self.loc: list[int] = loc
        self.opened: bool = opened
        self.surface = pygame.Surface(CARD_SIZE)

        # 클래스 변수 정의
        self.move_speed: list[list[int]] = []
        self.sizeX_flipping: list[Optional[int]] = []
        self.size: list[int] = CARD_SIZE.copy()
        self.is_flipping: bool = False
        self.is_flip_up: bool = True

    def set_destination(self, destination: list[int], frame: int = FPS, accel: int = 5) -> None:
        """
        카드 전달 시의 속도를 계산하는 함수.\n
        매 프레임 움직여야하는 거리를 [x, y] 형태로 move_speed 리스트에 저장한다.\n
        각 프레임, 남은 거리의 1/accel 만큼 움직인다.

        :param destination: 목표 위치. [x, y] 형태로 입력받는다.
        :param frame: 움직임이 지속될 프레임 수. 다만 accel 값에 따라 frame 수를 다 채우지 못하고 멈출 수 있다. 기본값 상수 FPS.
        :param accel: 움직임의 가속도. 높을 수록 느려진다. 기본값 5.
        :return: None
        """
        # 각 좌표가 양의 방향인지 여부 확인
        is_positive_direction = [self.loc[xy] <= destination[xy] for xy in range(2)]
        # 각 좌표의 이동 거리의 절댓값을 구함
        displace = [(destination[xy] - self.loc[xy]) if is_pd else (destination[xy] - self.loc[xy]) * -1
                    for xy, is_pd in enumerate(is_positive_direction)]
        # 속도 구하기
        speed = [[], []]
        for xy in range(2):
            speed[xy].append(displace[xy] // accel)
            for i in range(1, frame - 1):
                speed[xy].append(speed[xy][i - 1] * (accel - 1) // accel)
            speed[xy].append(displace[xy] - sum(speed[xy]))
            speed[xy].sort(reverse=True)
        # [x, y] 리스트 형태로 저장
        self.move_speed = [[moment[0], moment[1]] for moment in zip(*speed)]

    def frame_move(self) -> None:
        if len(self.move_speed) > 0:
            for xy in range(2):
                self.loc[xy] += self.move_speed[0][xy]
            self.move_speed.remove(self.move_speed[0])

    def flip(self) -> None:
        self.is_flipping = True
        self.is_flip_up = True
        grad: list[Optional[int]] = [round(CARD_SIZE[0] / 10 * n) for n in range(1, 10)] + [CARD_SIZE[0]]
        grad.sort(reverse=True)
        grad += [None]
        grad += [round(CARD_SIZE[0] / 10 * n) for n in range(1, 10)] + [CARD_SIZE[0]]
        self.sizeX_flipping = grad
        print(self.sizeX_flipping)

    def flipping(self):
        """넘겨지는 애니메이션 효과를 줌"""
        if len(self.sizeX_flipping) > 0:
            if self.sizeX_flipping[0] is None:
                self.is_flip_up = False
                self.opened = not self.opened
                self.sizeX_flipping[0] = 0
            self.size[0] = self.sizeX_flipping.pop(0)
        else:
            self.is_flipping = False
        self.surface = pygame.transform.scale(self.imagefile(), (self.size[0], CARD_SIZE[1]))

    def image_blit(self, display: pygame.Surface) -> None:
        """이미지 출력"""
        if self.is_flipping:
            self.flipping()
            display.blit(self.surface, self.coordinate())
        else:
            display.blit(self.imagefile(), self.coordinate())

    def imagefile(self) -> pygame.Surface:
        """이미지 파일 참조"""
        if self.opened:
            return self.imagefiles[self.mark][self.number]
        else:
            return self.imagefiles[0][0]

    def coordinate(self) -> list[int]:
        """이미지 입력을 위한 좌표 입력"""
        return [self.loc[xy] + (CARD_SIZE[xy] - self.size[xy]) // 2 for xy in range(2)]

# 프로그램 내 모듈
import pygame

from module.class_card import *
from module.class_chip import *


class CardBundle:
    def __init__(self):
        self.card_list: list[Card] = []

    def number(self) -> int:
        return len(self.card_list)

    def clear(self, animation: bool = True) -> None:
        """남은 카드를 모두 버림"""
        self.card_list = []

    def add_card(self, *cards: Card) -> None:
        """
        입력된 카드들을 목록에 넣음

        :param cards: 입력할 카드, 1개부터 여러개 넣을 수 있음
        :return: None
        """
        for card in cards:
            # print(f'log({pygame.time.get_ticks()}) Card "{Card.mark_names[card.mark]} {Card.number_names[card.number]}" Added')
            self.card_list.append(card)

    def pop_card(self, index: int = None) -> Optional[Card]:
        """
        카드 목록에서 1장을 뽑아 반환함 \n
        반환된 카드는 클래스 내에서 삭제됨

        :param index: 입력할 경우 그 순서에 있는 카드, 입력하지 않을 경우 마지막 카드를 반환함
        :return: Card. 클래스 내에 카드가 없었을 경우 None
        """
        if self.number() == 0:
            return
        if index is None or index >= self.number():
            index = self.number() - 1
        # print(f'log({pygame.time.get_ticks()}) Card "{Card.mark_names[self.card_list[index].mark]} {Card.number_names[self.card_list[index].number]}" Poped')
        return self.card_list.pop(index)


class Deck(CardBundle):
    deck_base_image = pygame.image.load('./card_images/card_base.png')

    def __init__(self, frame, fill: bool = True):
        super().__init__()
        self.loc = DECK_LOCATION.copy()
        self.FramePerSec = frame
        self.filling = False
        self.shffling = False
        if fill:
            self.fill()

    def pop_card(self, index: int = None) -> Optional[Card]:
        if self.number() == 0:
            self.fill()
        if index is None or index >= self.number():
            index = self.number() - 1
        print(f'log({pygame.time.get_ticks()}) Card "{Card.mark_names[self.card_list[index].mark]} {Card.number_names[self.card_list[index].number]}" Poped')
        card = self.card_list.pop(index)
        card.loc[1] += 20
        return card

    def fill(self, decks: int = 4, animation: bool = True) -> None:
        """
        덱을 새로운 카드로 채우고 섞음

        :param decks: 채울 덱의 수. 1덱은 52장이며 입력하지 않을 경우 기본값 1.
        :param clear: 새로운 카드를 넣기 전에 덱을 비울 것인지 확인. 기본값 False.
        :param animation: 애니메이션 출력 여부
        :return: None
        """
        self.filling = True
        i, temp = 0, 0
        for n in range(decks):
            for mark in range(1, 4 + 1):
                for number in range(1, 13 + 1):
                    self.card_list.append(Card(mark, number, *[DECK_LOCATION[0] - i, -93], False))
                    temp += 1
                    if temp == 3:
                        i += 1
                        temp = 0
        del i, temp
        if animation:
            direction = [1 if DECK_LOCATION[xy] >= self.card_list[0].loc[xy] else -1 for xy in range(2)]
            while True:
                self.FramePerSec.tick(FPS)

                displace = [abs(DECK_LOCATION[xy] - self.card_list[0].loc[xy]) for xy in range(2)]
                if displace == [0, 0]:
                    break

                for xy in range(2):
                    if displace[xy] == 0:
                        pass
                    elif displace[xy] < 4:
                        for card in self.card_list:
                            card.loc[xy] += displace[xy] * direction[xy]
                    else:
                        for card in self.card_list:
                            card.loc[xy] += displace[xy] // 4 * direction[xy]
        self.filling = False
        self.shuffle()

    def shuffle(self) -> None:
        random.shuffle(self.card_list)

    def images_blit(self, display: pygame.Surface) -> None:
        display.blit(self.deck_base_image, self.loc)
        if not self.filling and not self.shffling:
            coordinate = self.loc.copy()
            temp = 0
            for card in self.card_list:
                card.loc = coordinate.copy()
                card.image_blit(display, deck=True)
                temp += 1
                if temp == 3:
                    coordinate[0] -= 1
                    temp = 0
        else:
            for card in self.card_list:
                card.image_blit(display, deck=True)


class Hand(CardBundle):
    def __init__(self, x: int, y: int):
        super().__init__()

        self.loc = [x, y]

        # 게임 중 상황 변수
        self.is_standed = False
        self.is_splited = False
        self.is_doubledown = False
        self.is_surrendered = False

        self.bet = 0
        self.insurance_bet = 0

    def point(self) -> int:
        """패에 있는 카드의 점수를 계산한다. A가 있을 경우 21을 넘지 않는 가장 높은 값으로 계산된다."""
        result = 0
        count_ace = 0
        # A는 11, J~K는 10으로 계산하여 합을 계산
        for number in [element.number for element in self.card_list]:
            if number == 1:
                count_ace += 1
                result += 11
            elif number > 10:
                result += 10
            else:
                result += number
        # 21을 넘을 경우 21 이하가 되도록 A를 1로 계산할 수 있다.
        while count_ace > 0 and result > 21:
            count_ace -= 1
            result -= 10

        return result

    def is_bust(self) -> bool:
        return self.point() > 21

    def is_blackjack(self) -> bool:
        return self.number() == 2 and self.point() == 21 and not self.is_splited

    def can_split(self) -> bool:
        return self.number() == 2 and self.card_list[0].number == self.card_list[1].number

    def next_loc(self) -> list:
        return [self.loc[0] + (self.number() * 10), self.loc[1]]

    def images_blit(self, display: pygame.Surface) -> None:
        coordinate = self.loc.copy()
        for card in self.card_list:
            card.loc = coordinate.copy()
            card.image_blit(display)
            coordinate[0] += 10

    def chip_blit(self, display: pygame.Surface) -> None:
        Chip.chip_blit(self.bet, display, (self.loc[0] + 10, self.loc[1] + 80))

    def insurance_blit(self, display: pygame.Surface) -> None:
        if self.insurance_bet > 0:
            Chip.chip_blit(self.insurance_bet, display, (self.loc[0] + 10, self.loc[1] - 48))

    def reset(self) -> None:
        self.clear()
        self.is_standed = False
        self.is_splited = False
        self.is_doubledown = False
        self.is_surrendered = False
        self.bet = 0
        self.insurance_bet = 0

# 프로그램 내 모듈
from module.class_card import *


class CardBundle:
    def __init__(self):
        self.card_list: list[Card] = []

    def number(self) -> int:
        return len(self.card_list)

    def clear(self, animation: bool = True) -> None:
        """남은 카드를 모두 버림"""
        self.card_list = []
        if animation:
            pass

    def add_card(self, *cards: Card) -> None:
        """
        입력된 카드들을 목록에 넣음

        :param cards: 입력할 카드, 1개부터 여러개 넣을 수 있음
        :return: None
        """
        for card in cards:
            print(f'log({pygame.time.get_ticks()}) Card "{Card.mark_names[card.mark]} {Card.number_names[card.number]}" Added')
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
        print(f'log({pygame.time.get_ticks()}) Card "{Card.mark_names[self.card_list[index].mark]} {Card.number_names[self.card_list[index].number]}" Poped')
        return self.card_list.pop(index)


class Deck(CardBundle):
    def __init__(self, fill: bool = True):
        super().__init__()
        self.loc = DECK_LOCATION.copy()
        if fill:
            self.fill()

    def pop_card(self, index: int = None) -> Optional[Card]:
        if self.number() == 0:
            self.fill()
        if index is None or index >= self.number():
            index = self.number() - 1
        print(f'log({pygame.time.get_ticks()}) Card "{Card.mark_names[self.card_list[index].mark]} {Card.number_names[self.card_list[index].number]}" Poped')
        return self.card_list.pop(index)

    def fill(self, decks: int = 1, clear: bool = False) -> None:
        """
        덱을 새로운 카드로 채우고 섞음

        :param decks: 채울 덱의 수. 1덱은 52장이며 입력하지 않을 경우 기본값 1.
        :param clear: 새로운 카드를 넣기 전에 덱을 비울 것인지 확인. 기본값 False.
        :return: None
        """
        if clear:
            self.clear()
        for n in range(decks):
            for mark in range(1, 4 + 1):
                for number in range(1, 13 + 1):
                    self.card_list.append(Card(mark, number, *DECK_LOCATION, False))
        self.shuffle()

    def shuffle(self, animation: bool = True) -> None:
        random.shuffle(self.card_list)
        if animation:
            pass

    def images_blit(self, display: pygame.Surface) -> None:
        coordinate = self.loc.copy()
        temp = 0
        for card in self.card_list:
            card.loc = coordinate.copy()
            card.image_blit(display)
            temp += 1
            if temp == 3:
                coordinate[1] -= 1
                temp = 0


class Hand(CardBundle):
    def __init__(self, x: int, y: int):
        super().__init__()

        self.loc = [x, y]

        # 게임 중 상황 변수
        self.is_standed = False
        self.is_splited = False
        self.is_doubledown = False

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

    def copy2split(self) -> Any:
        """
        스플릿시 핸드를 2개로 분리하는 메소드\n
        마지막 카드를 뽑아 Hand 클래스를 생성한다.

        :return: Card
        """
        self.is_splited = True
        new_hand = Hand(self.loc[0] + 10, self.loc[1])
        new_hand.add_card(self.pop_card())
        new_hand.is_splited = True
        return new_hand

    def images_blit(self, display: pygame.Surface) -> None:
        coordinate = self.loc.copy()
        for card in self.card_list:
            card.loc = coordinate.copy()
            card.image_blit(display)
            coordinate[0] += 10

    def reset(self) -> None:
        self.clear()
        self.is_standed = False
        self.is_splited = False
        self.is_doubledown = False

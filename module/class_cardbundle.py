from class_card import *
import random


class CardBundle:
    def __init__(self):
        self.card_list: list[Card] = []

    def number(self) -> int:
        return len(self.card_list)

    def clear(self):
        self.card_list = []

    def pop_card(self, index: int = None) -> Optional[Card]:
        """
        카드 목록에서 1장을 뽑아 반환함 \n
        반환된 카드는 클래스 내에서 삭제됨

        :param index: 입력할 경우 그 순서에 있는 카드, 입력하지 않을 경우 마지막 카드를 반환함
        :return: Card. 클래스 내에 카드가 없었을 경우 None
        """
        if self.number() == 0:
            return
        if index is None:
            index = self.number() - 1
        return self.card_list.pop(0)


class Deck(CardBundle):
    def __init__(self, fill: bool = True):
        super().__init__()
        if fill:
            self.fill()

    def fill(self, decks: int = 1, clear: bool = False):
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
                    self.card_list.append(Card(mark, number, DECK_LOCATION, False))
        self.shuffle()

    def shuffle(self, animation: bool = True):
        random.shuffle(self.card_list)
        if animation:
            pass


class Hand(CardBundle):
    num_of_players = 0

    def __init__(self):
        super().__init__()
        self.turn_number = self.num_of_players
        self.num_of_players += 1

        self.loc = [None, None]

        # 게임 중 상황 변수
        self.is_splited = False

    def is_dealer(self) -> bool:
        return self.turn_number == 0

    def point(self):
        """패에 있는 카드의 점수를 계산한다. A가 있을 경우 21을 넘지 않는 가장 높은 값으로 계산된다."""
        result = 0
        count_ace = 0

        for number in [element.number for element in self.card_list]:
            if number == 1:
                count_ace += 1
                result += 11
            elif number > 10:
                result += 10
            else:
                result += number

        while count_ace > 0 and result > 21:
            count_ace -= 1
            result -= 10

        return result

    def is_blackjack(self) -> bool:
        return self.number() == 2 and self.point() == 21 and not self.is_splited

    def add_card(self, *cards: Card):
        for card in cards:
            self.card_list.append(card)

    def copy2split(self) -> Any:
        self.is_splited = True
        new_hand = Hand()
        new_hand.add_card(self.pop_card())
        return new_hand

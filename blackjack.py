from typing import Final
import random


class Card:
    SPADE: Final = 1
    HEART: Final = 2
    DIAMOND: Final = 3
    CLOVER: Final = 4

    MARK = ['#', '♠', '♥', '◆', '♣']
    NUMBER = ['#', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self, mark, number: int, opened=False):
        try:
            if 1 <= int(mark) <= 4:
                self.mark = int(mark)
            else:
                print("Ingame Error: Card Mark Setting Error")
                self.mark = 0
        except ValueError:
            if mark == "SPADE" or mark == "spade":
                self.mark = 1
            elif mark == "HEART" or mark == "heart":
                self.mark = 2
            elif mark == "DIAMOND" or mark == "diamond":
                self.mark = 3
            elif mark == "CLOVER" or mark == "clover":
                self.mark = 4
            else:
                print("Ingame Error: Card Mark Setting Error")
                self.mark = 0
        if 1 <= number <= 13:
            self.number = number
        else:
            print("Ingame Error: Card Number Setting Error")
            self.number = 0
        self.open = opened

    def card_open(self):
        self.open = True

    def card_close(self):
        self.open = False

    def __str__(self):
        return self.MARK[self.mark] + self.NUMBER[self.number]

    def __repr__(self):
        return self.MARK[self.mark] + self.NUMBER[self.number]

    def shape(self) -> str:
        if self.open:
            return self.MARK[self.mark] + self.NUMBER[self.number]
        else:
            return '▒▒'


class Cards:
    def __init__(self):
        self.list: list[Card] = []

    def number(self):
        return len(self.list)

    def reset(self):
        self.list = []

    @classmethod
    def one_deck(cls) -> list[Card]:
        temp = []
        for mark in range(1, 5):
            for number in range(1, 14):
                temp.append(Card(mark, number))
        return temp


class Deck(Cards):
    def __init__(self, decks=1):
        super(Deck, self).__init__()
        self.refill(decks)
        self.decks = decks

    def shuffle(self):
        random.shuffle(self.list)

    def draw(self, open=True) -> Card:
        if len(self.list) == 0:
            self.refill()
        if len(self.list) > 0:
            temp = self.list[0]
            self.list.remove(temp)
            temp.open = open
            return temp
        else:
            print("Ingame Error: There is not a card to draw in the deck")
            return None

    def refill(self, decks=None):
        if decks is None:
            decks = self.decks
        temp = Cards.one_deck()
        for i in range(decks):
            self.list = self.list + temp
        self.shuffle()

    def change_deck_number(self, num: int):
        self.decks = num


class Hand(Cards):
    def take(self, card: Card):
        self.list.append(card)

    def open(self, index=None):
        if index is None:
            for i in self.list:
                i.card_open()
        elif 0 < index < len(self.list):
            self.list[index].card_open()
        else:
            print("Ingame Error: Failure to open a card in hand")

    def close(self, index=None):
        if index is None:
            for i in self.list:
                i.card_close()
        elif 0 < index < len(self.list):
            self.list[index].card_close()
        else:
            print("Ingame Error: Failure to close a card in hand")

    def result(self) -> int:
        if len(self.list) == 0:
            return 0
        aces = 0
        for n in self.list:
            if n.number == 1:
                aces += 1
        result = sum([(n.number if n.number <= 10 else 10) for n in self.list]) + (aces * 10)
        if aces > 0:
            for i in range(aces):
                if result > 21:
                    result -= 10
        return result

    def is_blackjack(self) -> bool:
        if len(self.list) == 2 and self.result() == 21:
            return True
        else:
            return False


def fullhand_shape(bundle: Hand) -> str:
    temp = ""
    if bundle.number() > 0:
        for i in bundle.list:
            temp += (i.shape() + ' ')
        temp = temp[:-1]
    return temp


class Blackjack:
    DECKS = 1
    START_MONEY = 1000
    DEALER_MONEY_ON = False
    DEALER_MONEY = 100000

    def __init__(self):
        self.deck = Deck(self.DECKS)
        self.player = Hand()
        self.player_money = self.START_MONEY
        self.dealer = Hand()
        if self.DEALER_MONEY_ON:
            self.dealer_money = self.DEALER_MONEY
        self.status_string = ['','','']

    def print_status(self):
        for line in self.status_string:
            print(line)

    def new_status(self, text: str):
        for i in [0, 1]:
            self.status_string[i] = self.status_string[i + 1]
        self.status_string[2] = text

    def print_table(self):
        print()
        print("=" * 30)
        if self.dealer.is_blackjack():
            print("딜러 {}장 {}: {}".format(self.dealer.number(), "Blackjack", fullhand_shape(self.dealer)))
        else:
            print("딜러 {}장 {}: {}".format(self.dealer.number(), self.dealer.result(), fullhand_shape(self.dealer)))
        if self.DEALER_MONEY_ON:
            print("딜러 소지금: ${}".format(self.dealer_money))
        print()
        print("덱 {}장".format(self.deck.number()))
        print()
        if self.player.is_blackjack():
            print("패 {}장 {}: {}".format(self.player.number(), "Blackjack", fullhand_shape(self.player)))
        else:
            print("패 {}장 {}: {}".format(self.player.number(), self.player.result(), fullhand_shape(self.player)))
        print("소지금: ${}".format(self.player_money))
        print("=" * 30)
        self.print_status()
        print("=" * 30)

    def hand_reset(self):
        self.player.reset()
        self.dealer.reset()

    def game_reset(self):
        self.deck.reset()
        self.deck.refill()
        self.hand_reset()

    def bet(self) -> int:
        self.new_status("새 게임을 시작하려면 베팅 금액을 입력하십시오...")
        while True:
            try:
                self.print_table()
                temp = int(input("베팅 금액 : "))
                if temp <= self.player_money:
                    self.player_money -= temp
                    if self.DEALER_MONEY_ON:
                        self.dealer_money += temp
                    return temp
                else:
                    self.new_status("소지금이 부족합니다.")
            except ValueError:
                self.new_status("잘못된 입력값입니다.")

    def command(self) -> bool:
        while True:
            self.print_table()
            temp = input("1)힛 2)스테이 : ")
            if temp == '1':
                return True
            elif temp == '2':
                return False

    def dealer_turn(self) -> bool:
        if self.dealer.result() >= 17:
            return False
        self.new_status("딜러 힛")
        self.dealer.take(self.deck.draw())
        if self.dealer.result() > 21:
            self.new_status("딜러 버스트")
        self.print_table()
        input()
        return True

    def winner_calc(self, player_bust: bool, dealer_bust: bool):
        PLAYER_WIN = 1
        DEALER_WIN = -1
        DRAW = 0
        if player_bust:
            return DEALER_WIN
        elif dealer_bust:
            return PLAYER_WIN
        elif self.player.result() > self.dealer.result():
            return PLAYER_WIN
        elif self.player.result() < self.dealer.result():
            return DEALER_WIN
        else:
            if self.player.is_blackjack() and not self.dealer.is_blackjack():
                return PLAYER_WIN
            elif not self.player.is_blackjack() and self.dealer.is_blackjack():
                return DEALER_WIN
            else:
                return DRAW

    def game_start(self, num=-1):
        self.game_reset()

        # 라운드
        while True:
            self.hand_reset()
            player_bust = False
            dealer_bust = False
            betting = self.bet()
            self.new_status("게임 시작!")
            self.dealer.take(self.deck.draw(False))
            self.player.take(self.deck.draw())
            self.dealer.take(self.deck.draw())
            self.player.take(self.deck.draw())

            # 턴
            while True:
                if self.command():
                    self.new_status("플레이어 힛")
                    self.player.take(self.deck.draw())
                    if self.player.result() > 21:
                        player_bust = True
                        self.new_status("플레이어 버스트")
                        self.print_table()
                        input()
                        self.dealer.open()
                        break
                    self.dealer.open()
                    self.dealer_turn()
                    if self.dealer.result() > 21:
                        dealer_bust = True
                        break
                else:
                    self.new_status("플레이어 스테이")
                    self.dealer.open()
                    break
            if not player_bust and not dealer_bust:
                while self.dealer_turn():
                    if self.dealer.result() > 21:
                        dealer_bust = True
                        break

            winner = self.winner_calc(player_bust, dealer_bust)

            # 정산
            if winner > 0:
                # 플레이어 승리
                if self.player.is_blackjack():
                    self.new_status("플레이어 블랙잭!")
                    betting = round(betting * 2.5)
                else:
                    self.new_status("플레이어 승리!")
                    betting *= 2
                if self.DEALER_MONEY_ON:
                    if self.dealer_money < betting:
                        betting = self.dealer_money
                    self.dealer_money -= betting
                self.player_money += betting
                self.new_status("소지금 +${}".format(betting))
            elif winner < 0:
                # 딜러 승리
                self.new_status("딜러 승리!")
            else:
                # 무승부
                self.new_status("푸시!")
                self.player_money += betting
                self.new_status("소지금 +${}".format(betting))

            self.print_table()
            input()


def main():
    game = Blackjack()
    game.game_start()
    pass


if __name__ == "__main__":
    main()

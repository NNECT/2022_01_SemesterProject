from class_cardbundle import *


class CardtoCard:
    def __init__(self):
        self.card_list: list[list[Card, list[int], Optional[Hand]]] = []

    def frame_work(self) -> bool:
        if len(self.card_list) == 0:
            return False
        for card in self.card_list:
            card[0].frame_move()
            if card[0].loc == card[1]:
                if card[2] is not None:
                    card[2].add_card(card[0])
                self.card_list.remove(card)
        return True

    def move(self, card: Card, destination: list[int], target: Optional[Hand] = None):
        self.card_list.append([card, destination, target])

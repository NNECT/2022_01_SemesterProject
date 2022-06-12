# 프로그램 내 모듈
from module.class_cardbundle import *
from module.class_button import *


class BlackjackMain:
    def __init__(self):
        pygame.init()

        # 초당 프레임 단위 설정
        self.FramePerSec = pygame.time.Clock()

        # 게임 창 설정
        self.GameDisplay = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Blackjack GUI")  # 창 이름 설정

        # 기본 값 설정
        self.font = pygame.font.SysFont('timesnewroman', 21, True, False)

        self.deck = Deck(self.FramePerSec, False)
        self.hands = [Hand(*HAND_LOCATION[i]) for i in range(2)]
        self.out_of_hand = []
        self.buttons = [Button(i + 1, *BUTTON_LOCATION[i], False) for i in range(5)]
        self.texts = []

        self.money = BASE_MONEY

        self.button_standby = False
        self.clicked_button = None
        self.is_evenmoney = False
        self.is_insuranced = False
        self.turn = 0
        self.turn_player = 0

        self.gameover = False

        # 메인 게임 로직 호출
        self.gamemain = threading.Thread(target=self.game_main)
        self.gamemain.start()

        # 디스플레이 출력
        while True:
            self.FramePerSec.tick(FPS)

            # 마우스 위치 추적
            mouse_loc = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if self.button_standby:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        for temp in self.buttons:
                            if temp.on_button(*event.pos) and temp.is_on:
                                print(
                                    f'log({pygame.time.get_ticks()}) Button "{Button.kinds[temp.kind]}{event.pos}" Click')  # log
                                self.clicked_button = temp
                                self.button_standby = False

            # 화면 출력
            self.GameDisplay.fill(COLOR_BACKGROUND)  # 배경색 채우기
            for temp in self.buttons:
                if not self.button_standby:
                    temp.image_blit(self.GameDisplay, 0)
                elif not temp.on_button(*mouse_loc):
                    temp.image_blit(self.GameDisplay, 1)
                else:
                    temp.image_blit(self.GameDisplay, 2)

            # 개체 출력
            Chip.chiptower_blit(self.money, self.GameDisplay)
            self.chip_number = self.font.render(str(self.money), True, (0, 0, 0))
            self.GameDisplay.blit(self.chip_number, CHIPNUMBER_LOCATION)
            self.deck.images_blit(self.GameDisplay)
            for hand in self.hands:
                hand.images_blit(self.GameDisplay)
                hand.chip_blit(self.GameDisplay)
                hand.insurance_blit(self.GameDisplay)
            for card in self.out_of_hand:
                card.image_blit(self.GameDisplay)
            for text in self.texts:
                self.GameDisplay.blit(*text)
            if self.turn_player > 0:
                pygame.draw.line(self.GameDisplay, (0, 255, 0),
                                 [self.hands[self.turn_player].loc[0] - 10, self.hands[self.turn_player].loc[1] - 1],
                                 [self.hands[self.turn_player].loc[0] - 10, self.hands[self.turn_player].loc[1] + 72], 5)

            pygame.display.update()

            if self.gameover:
                self.GameDisplay.blit(pygame.image.load('./other_images/game_over.png'), GAME_OVER_LOCATION)
                pygame.display.update()
                time.sleep(5)
                pygame.quit()
                sys.exit()

    # 메인 알고리즘
    def game_main(self):
        self.deck.fill()

        while True:
            # 초기화
            for hand in self.hands:
                hand.reset()
            if len(self.hands) > 2:
                del self.hands[2:]
            for button in self.buttons:
                button.is_on = False
                if button.kind in [INSURANCE, EVENMONEY]:
                    button.kind = SURRENDER

            self.button_standby = False
            self.clicked_button = None
            self.is_evenmoney = False
            self.is_insuranced = False
            self.turn = 0

            # 라운드 시작
            for i in range(DEAL_MONEY):
                time.sleep(0.2)
                self.money -= 1
                self.hands[1].bet += 1

            while True:
                self.turn += 1

                # 카드 분배
                if self.turn == 1:  # 2장 버리기
                    time.sleep(0.5)
                    for i in range(2):
                        self.card_move(self.deck.pop_card(), [-50, HAND_LOCATION[0][1]])
                if self.deal():
                    break  # 플레이어 버스트시 즉시 종료
                if self.turn == 1:  # 첫 턴 1장 추가 분배
                    self.deal(True)

                if self.hands[0].is_bust():  # 딜러 버스트
                    self.text_blit("Bust", self.hands[0])
                    break
                if self.hands[0].point() > 16:
                    self.hands[0].is_standed = True
                if self.hands[0].is_standed and self.hands[0].card_list[1].opened:
                    for hand in self.hands[1:]:
                        if self.calc_win(hand) > 0:
                            hand.is_standed = True

                # 게임 진행
                if self.running_game():
                    self.turn_player = 0
                    break  # 종료 조건 만족시 탈출
                self.turn_player = 0

                if self.turn == 1:
                    self.hands[0].card_list[1].opened = True
                    if self.hands[0].is_blackjack():
                        break

                if self.round_end():
                    break

            self.calculation()
            time.sleep(1)
            if self.money < DEAL_MONEY:
                break
            time.sleep(1)
            self.table_clear()

        self.gameover = True

    def running_game(self) -> bool:
        split = True
        while split:
            split = False
            for i, hand in enumerate(self.hands[1:]):
                if hand.is_standed or hand.is_surrendered or hand.is_bust():
                    continue

                self.turn_player = i + 1

                if self.button_set(i + 1):  # 버튼 세팅
                    return True
                if hand.is_standed:
                    continue
                if self.wait_click():  # 버튼 클릭 대기
                    return True

                self.turn_player = 0

                for button in self.buttons:  # 버튼 초기화
                    button.is_on = False
                    if button.kind in [INSURANCE, EVENMONEY]:
                        button.kind = SURRENDER

                clicked_button = self.clicked_button.kind
                self.clicked_button = None

                if clicked_button == HIT:
                    pass
                elif clicked_button == STAND:
                    hand.is_standed = True
                elif clicked_button == DOUBLEDOWN:
                    for j in range(DEAL_MONEY):
                        time.sleep(0.2)
                        self.money -= 1
                        hand.bet += 1
                    hand.is_doubledown = True
                elif clicked_button == SURRENDER:
                    hand.is_surrendered = True
                    if self.player_out():
                        return True
                elif clicked_button == EVENMONEY:
                    self.is_evenmoney = True
                    return True
                elif clicked_button == SPLIT:
                    self.hands.append(Hand(*HAND_LOCATION[2]))
                    for sp in self.hands[1:]:
                        sp.is_splited = True
                    self.hands[2].add_card(self.card_move(self.hands[1].card_list.pop(), self.hands[2].next_loc()))
                    for j in range(DEAL_MONEY):
                        time.sleep(0.2)
                        self.money -= 1
                        self.hands[2].bet += 1
                    self.deal(split=True)
                    split = True
                    break
        return False

    def round_end(self):
        end = True
        for hand in self.hands:
            if not hand.is_standed and not hand.is_surrendered and not hand.is_bust():
                end = False
        return end

    def player_out(self):
        out = True
        for hand in self.hands[1:]:
            if not hand.is_surrendered and not hand.is_bust():
                out = False
        return out

    def deal(self, last_close=False, split=False) -> bool:
        for hand in self.hands[1:]:
            if not hand.is_standed and not hand.is_surrendered and not hand.is_bust():
                time.sleep(0.5)
                temp = self.card_move(self.deck.pop_card(), hand.next_loc())
                hand.add_card(temp)
                time.sleep(0.1)
                temp.opened = True
                if hand.is_bust():
                    self.text_blit("Bust", hand)
                if self.player_out():
                    return True
                if hand.is_doubledown:
                    hand.is_standed = True
        if not split:
            if not self.hands[0].is_standed:
                time.sleep(0.5)
                temp = self.card_move(self.deck.pop_card(), self.hands[0].next_loc())
                self.hands[0].add_card(temp)
                if last_close:
                    pass
                else:
                    time.sleep(0.1)
                    temp.opened = True
        return False

    def card_move(self, card: Card, dest, *other_cards) -> Card:
        self.out_of_hand.append(card)
        # 각 양의 방향인지 확인
        direction = [1 if dest[xy] >= card.loc[xy] else -1 for xy in range(2)]
        while True:
            self.FramePerSec.tick(FPS)

            for other in other_cards:
                other.loc = card.loc.copy()

            displace = [abs(dest[xy] - card.loc[xy]) for xy in range(2)]
            if displace == [0, 0]:
                break

            for xy in range(2):
                if displace[xy] == 0:
                    pass
                elif displace[xy] < 4:
                    card.loc[xy] += displace[xy] * direction[xy]
                else:
                    card.loc[xy] += displace[xy] // 4 * direction[xy]

        self.out_of_hand.remove(card)
        return card

    def button_set(self, num: int = 1) -> bool:
        if len(self.hands) == 2 and self.hands[1].is_blackjack():
            self.text_blit("Blackjack", self.hands[1])
            if not self.hands[0].card_list[0].number == 1 and not self.hands[0].card_list[0].number >= 10:
                # 정산 후 새 게임
                return True
            elif not self.hands[0].card_list[0].number == 1:
                self.hands[0].card_list[1].opened = True
                return True
            else:
                for button in self.buttons:
                    if button.kind == STAND:
                        button.is_on = True
                    elif button.kind == SURRENDER:
                        button.kind = EVENMONEY
                        button.is_on = True
        elif self.hands[num].point() == 21:
            self.hands[num].is_standed = True
        else:
            for button in self.buttons:
                if button.kind == HIT:
                    if self.hands[num].point() < 21:
                        button.is_on = True
                elif button.kind == DOUBLEDOWN:
                    if self.hands[num].point() < 21 and self.money >= DEAL_MONEY:
                        button.is_on = True
                elif button.kind == STAND:
                    button.is_on = True
                    if self.hands[0].is_standed and self.hands[0].card_list[1].opened and self.calc_win(self.hands[num]) < 0:
                        button.is_on = False
                elif button.kind == SURRENDER:
                    if not self.hands[0].card_list[1].opened and self.hands[0].card_list[0].number == 1:
                        button.kind = INSURANCE
                        if self.money >= DEAL_MONEY / 2:
                            button.is_on = True
                    else:
                        button.is_on = True
                elif button.kind == SPLIT:
                    if len(self.hands) == 2 and self.hands[1].can_split() and self.money >= DEAL_MONEY:
                        button.is_on = True

    def wait_click(self) -> bool:
        self.button_standby = True
        while True:
            self.FramePerSec.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            if not self.button_standby:
                if self.clicked_button.kind == INSURANCE:
                    for i in range(DEAL_MONEY // 2):
                        time.sleep(0.2)
                        self.money -= 1
                        self.hands[1].insurance_bet += 1
                    time.sleep(0.2)
                    if self.hands[0].is_blackjack():
                        self.hands[0].card_list[1].opened = True
                        # 정산 후 새 게임
                        self.is_insuranced = True
                        return True
                    else:
                        # 그대로 게임
                        self.text_blit("No Blackjack", self.hands[0])
                        self.hands[1].insurance_bet = 0
                        self.buttons[SURRENDER - 1].kind = SURRENDER
                        self.button_standby = True
                        continue
                else:
                    return False

    def calculation(self):
        if self.hands[0].is_blackjack() and not self.is_evenmoney:
            self.text_blit("Blackjack", self.hands[0])

        for hand in self.hands[1:]:
            prize = 0

            if self.is_insuranced:
                self.text_blit("Insurance", hand)

                win = INSURANCE
                hand.insurance_bet = 0

            elif self.is_evenmoney:
                self.text_blit("Evenmoney", hand)

                win = EVENMONEY
                prize = hand.bet

            elif hand.is_surrendered:
                # LOSE
                win = -1
                score_text = '(Surrender)'

            elif hand.is_bust():
                # LOSE
                win = -1
                score_text = '(Bust)'

            elif self.hands[0].is_bust():
                # WIN
                win = 1
                prize = hand.bet
                score_text = '(Dealer Bust)'

            else:
                check = self.calc_win(hand)
                score_text = f'({hand.point()}:{self.hands[0].point()})'
                if check > 0:
                    # WIN
                    win = 1
                    prize = int(hand.bet * check)
                    if hand.is_blackjack():
                        score_text = '(Blackjack)'

                elif check == 0:
                    # PUSH
                    win = 0

                else:
                    # LOSE
                    win = -1
                    if self.hands[0].is_blackjack():
                        score_text = '(Dealer Blackjack)'

            if win == 1 or win == EVENMONEY:
                if win == 1:
                    self.text_blit("WIN " + score_text, hand)

                for i in range(prize):
                    time.sleep(0.2)
                    hand.bet += 1
                time.sleep(0.5)
                for i in range(hand.bet):
                    time.sleep(0.2)
                    hand.bet -= 1
                    self.money += 1

            elif win == 0 or win == INSURANCE:
                if win == 0:
                    self.text_blit("PUSH " + score_text, hand)

                for i in range(hand.bet):
                    time.sleep(0.2)
                    hand.bet -= 1
                    self.money += 1

            elif win == -1:
                self.text_blit("LOSE " + score_text, hand)

                hand.bet = 0

    def calc_win(self, hand):
        if hand.is_blackjack():
            if not self.hands[0].is_blackjack():
                return 1.5
            else:
                return 0
        else:
            if self.hands[0].is_blackjack():
                return -1

        if hand.point() > self.hands[0].point():
            return 1
        elif hand.point() == self.hands[0].point():
            return 0
        else:
            return -1

    def table_clear(self):
        discard_list = []
        for i in range(len(self.hands)):
            num = len(self.hands) - i - 1
            if num == 0:
                break
            while self.hands[num].number() > 1:
                temp = self.hands[num].pop_card()
                temp.opened = False
                self.out_of_hand.append(temp)
                self.card_move(temp, [temp.loc[0] - 10, temp.loc[1]], *discard_list)
                discard_list.append(temp)
            temp = self.hands[num].pop_card()
            temp.opened = False
            self.out_of_hand.append(temp)
            self.card_move(temp, [self.hands[num - 1].next_loc()[0] - 10, self.hands[num - 1].next_loc()[1]], *discard_list)
            discard_list.append(temp)
        while self.hands[0].number() > 1:
            temp = self.hands[0].pop_card()
            temp.opened = False
            self.out_of_hand.append(temp)
            self.card_move(temp, [temp.loc[0] - 10, temp.loc[1]], *discard_list)
            discard_list.append(temp)
        temp = self.hands[0].pop_card()
        temp.opened = False
        self.out_of_hand.append(temp)
        self.card_move(temp, [-50, HAND_LOCATION[0][1]], *discard_list)
        discard_list.append(temp)

        for card in discard_list:
            self.out_of_hand.remove(card)

    def text_blit(self, txt: str, hand: Hand) -> None:
        text = [self.font.render(txt, True, (0, 0, 0)), (hand.loc[0] + TEXT_LOCATION[0], hand.loc[1] + TEXT_LOCATION[1])]
        self.texts.append(text)
        for i in range(20):
            self.FramePerSec.tick(FPS)
            text[1] = (hand.loc[0] + TEXT_LOCATION[0], hand.loc[1] + TEXT_LOCATION[1] - (i // 2))
        for i in range(60):
            self.FramePerSec.tick(FPS)
            text[1] = (hand.loc[0] + TEXT_LOCATION[0], hand.loc[1] + TEXT_LOCATION[1] - 10)
        self.texts.remove(text)


def main():
    BlackjackMain()


if __name__ == "__main__":
    main()

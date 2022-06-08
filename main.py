import threading

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

        self.deck = Deck()
        self.hands = [Hand(*HAND_LOCATION[i]) for i in range(2)]
        self.buttons = [Button(i + 1, *BUTTON_LOCATION[i]) for i in range(6)]
        self.texts = []

        self.button_standby = False
        self.clicked_button = None

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
                            if temp.on_button(*event.pos):
                                self.clicked_button = temp
                                print(f'log({pygame.time.get_ticks()}) Button "{Button.kinds[self.clicked_button.kind]}{event.pos}" Click')  # log

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
            self.deck.images_blit(self.GameDisplay)
            for hand in self.hands:
                hand.images_blit(self.GameDisplay)
            for text in self.texts:
                self.GameDisplay.blit(text, (400, 400))

            pygame.display.update()

    # 메인 알고리즘
    def game_main(self):
        self.texts.append(self.font.render("Blackjack", True, (0, 0, 0)))
        # time.sleep(2)
        for i in range(2):
            time.sleep(1)
            temp = self.deck.pop_card()
            self.hands[0].add_card(temp)
            time.sleep(0.2)
            temp.opened = True


def main():
    BlackjackMain()


if __name__ == "__main__":
    main()

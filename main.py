import sys
from module.class_cardbundle import *


class BlackjackMain():
    def __init__(self):
        pygame.init()

        # 초당 프레임 단위 설정
        FramePerSec = pygame.time.Clock()

        # 게임 창 설정
        GameDisplay = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Blackjack GUI")  # 창 이름 설정

        work_table = []

        deck = Deck()
        hands = [Hand(HAND_LOCATION[i]) for i in range(3)]

        play1 = Card(HEARTS, ACE, [screen_width // 2, screen_height // 5], opened=False)
        play1.set_destination([screen_width // 2, screen_height * 4 // 5])
        next_event_time = now() + 1000

        while True:
            FramePerSec.tick(FPS)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            play1.frame_move()

            if can_next_event(next_event_time):
                if not play1.opened:
                    play1.flip()
                    next_event_time = now() + (1000 * 21 // FPS)

            # 화면 출력
            GameDisplay.fill(COLOR_BACKGROUND)  # 배경색 채우기
            play1.image_blit(GameDisplay)
            # print(pygame.time.get_ticks())

            pygame.display.update()


def main():
    BlackjackMain()


if __name__ == "__main__":
    main()

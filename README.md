Blackjack Python GUI Game Program 
====
###### 수학과 이어진: _2022년 1학기 프로그래밍원리와실습 프로젝트_ 
***


## 프로그램 설명 
이 프로그램은 카드게임 블랙잭을 할 수 있는 프로그램이다.\
Python 3.10 Anaconda 인터프리터를 통해 제작되었으며, pygame 패키지를 사용하여 GUI 환경으로 구축되었다.


## 블랙잭 룰 설명 
적용된 게임의 룰을 설명한다.

### 1. 기본 룰 
플레이어가 일정 금액을 베팅한 후, 플레이어와 딜러는 2장 이상의 카드를 순서대로 받아 어느쪽이 그 합이 높은지 비교한다.\
플레이어의 합이 높으면 베팅한 금액만큼을 추가로 받고, 아니라면 베팅한 금액을 그대로 잃는다.
#### 계산법 
**J**, **Q**, **K**는 10으로 계산한다.\
**A**는 1 또는 11 중 원하는 값으로 계산한다.

### 2. 게임 내 용어 및 상세 룰 
`힛(Hit)` : 자신의 차례에 카드를 1장 더 받는다.\
`스탠드(Stand)` : 카드를 받는 것을 멈춘다.\
`버스트(Bust)` : 숫자의 합이 21점을 넘으면 즉시 패배한다.\
`푸시(Push)` : 플레이어와 딜러가 무승부일 때, 베팅한 금액을 돌려받는다.\
`블랙잭(Blackjack)` : 첫 패 2장이 **10**, **J**, **Q**, **K** 중 1장과 **A** 1장으로 21점을 만들 경우 같은 21점보다 높은 점수를 가진 것으로 취급한다.
블랙잭으로 게임에서 이겼을 때, 베팅액의 0.5배의 금액을 더 받는다.\

#### 특수 룰 
`서렌더(Surrender)` : 자신의 차례에 게임을 포기하고 베팅한 금액의 절반을 돌려받을 수 있다.\
`스플릿(Split)` : 첫 카드 2장이 서로 같은 숫자일 때, 이미 베팅한 금액과 같은 금액을 더 베팅하고 자신의 패를 둘로 나눌 수 있다.
따라서 플레이어는 2개의 게임을 동시에 2개 진행하게 된다.
단, 이후 블랙잭과 같은 패가 나와도 첫 카드 2장이 아니므로 블랙잭으로 취급하지 않는다.
_이 게임에서는 스플릿은 **한 번만** 할 수 있다._\
`더블다운(Double Down)` : 자신의 차례에 이미 베팅한 금액과 같은 금액을 더 베팅할 수 있다.
이후 카드를 1장만 더 받는다.\
`인셔런스(Insurance)` : 딜러의 공개된 첫 카드가 **A**일 때, 베팅한 금액의 절반을 지불하고 딜러의 **블랙잭**에 대비한 보험을 들 수 있다.
딜러가 블랙잭일 경우, 베팅한 금액을 돌려받는다.\
`이븐머니(Even Money)` : 자신이 **블랙잭**일 때 딜러의 공개된 첫 카드가 **A**일 경우, 베팅한 금액만큼을 승리금으로 받고 게임을 종료할 수 있다.

#### 딜러 룰 
딜러는 플레이어의 첫 차례가 끝날 때까지 카드 1장을 비공개한다.\
딜러는 숫자의 합이 17 이상이 될 때까지 힛을 반복한다.


## 프로그램 구성


### 작업로그 
    2022-05-17  프로젝트 시작
                pygame 패키지 사용을 위해 새로운 인터프리터 구성
    2022-05-18  콘솔창에서 돌아가는 테스트용 블랙잭 코드 작성
    2022-05-19  README.md 정리(프로그램 설명, 게임 룰) 및 작업로그 작성 시작
                pygame 이미지 개체 출력 테스트
                카드배분 애니메이션 속도 함수 작성
                Card 클래스 작성
                Card 클래스를 통한 카드이미지 출력 시스템 구축
                카드배분 애니메이션 코드 작성
                카드플립 애니메이션 코드 작성
                variable.py(상수), config.py(프로그램설정) 파일 생성
    2022-05-20  카드 여러장을 관리하는 CardBundle 클래스 작성
                Deck, Hand 서브클래스 작성
                해당 클래스들의 기본적인 기능 작성
                Hand.Split() 작성
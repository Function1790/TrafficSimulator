import pygame
import random as r
import math

start_road_pos = [
    [  # 상
        [328, 0],  # 전진
        [428, 0],  # 좌회전
        [328, 0]  # 우회전
    ],
    [  # 하
        [578, 900],
        [478, 900],
        [578, 900]
    ],
    [  # 좌
        [0, 588],
        [0, 475],
        [0, 588]
    ],
    [  # 우
        [900, 319],
        [900, 425],
        [900, 319]
    ],
]

stop_road_pos = [
    [556, 256],  # 상
    [346, 676],  # 하
    [248, 344],  # 좌
    [653, 552],  # 우
]

car_speed = 0.3

speed_list = [
    [  # 상
        (0, car_speed),  # 전진
        [(0, car_speed), (car_speed * 0.4, car_speed*0.6), (car_speed, 0)],  # 좌회전
        (-car_speed*0.8, car_speed*0.55)  # 우회전
    ],
    [  # 하
        (0, -car_speed),  # 전진
        [(0, -car_speed), (-car_speed * 0.4, -car_speed*0.6), (-car_speed, 0)],  # 좌회전
        (car_speed*0.8, -car_speed*0.6)  # 우회전
    ],
    [  # 좌
        (car_speed, 0),  # 전진
        [(car_speed, 0), (car_speed * 0.6, -car_speed*0.4), (0, -car_speed)],  # 좌회전
        (car_speed*0.5, car_speed*0.7)  # 우회전
    ],
    [  # 우
        (-car_speed, 0),  # 전진
        [(-car_speed, 0), (-car_speed * 0.6, car_speed*0.4), (0, car_speed)],  # 좌회전
        (-car_speed*0.5, -car_speed*0.7)  # 우회전
    ],
]

trafficSystemList = [  # 빨 좌 초
    [2, 2, 0, 0],
    [1, 1, 0, 0],
    [0, 0, 2, 2],
    [0, 0, 1, 1],
]

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

car_w = 80
car_h = 80

# 초기화 및 디스플레이 설정
pygame.init()
screen_width = 950
screen_height = 950
background = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("simulation")

# 이미지 불러오기
image_bg = pygame.image.load("image/intersection.png")
car_w = 40
car_h = 40
car_object = pygame.Rect((screen_width-car_w)/2,
                         screen_height-car_h, car_w, car_h)
car_img = pygame.image.load("image/car.png")
car_img = pygame.transform.scale(car_img, (car_w, car_h))

traffic_w = 100
traffic_h = 50
traffic_object = pygame.Rect((screen_width-traffic_w)/2,
                             screen_height-traffic_h, traffic_w, traffic_h)
trafficRed_img = pygame.image.load("image/lightRed.png")
trafficRed_img = pygame.transform.scale(trafficRed_img, (traffic_w, traffic_h))
trafficGreen_img = pygame.image.load("image/lightGreen.png")
trafficGreen_img = pygame.transform.scale(
    trafficGreen_img, (traffic_w, traffic_h))
trafficLeft_img = pygame.image.load("image/lightLeft.png")
trafficLeft_img = pygame.transform.scale(
    trafficLeft_img, (traffic_w, traffic_h))
trafficImg = [trafficRed_img, trafficLeft_img, trafficGreen_img]

# 이미지 가로, 세로 크기 구하기
size_bg_width = background.get_size()[0]  # 가로
size_bg_height = background.get_size()[1]  # 세로


# car움직임 조정
clock = pygame.time.Clock()
CarSize = 100

# Class


class TrafficLight:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.state = 0  # 0:빨간, 1:좌회전, 2:초록
        self.object = pygame.Rect(
            self.pos[0], self.pos[1], traffic_w, traffic_h)

    def draw(self):
        background.blit(trafficImg[self.state], self.object)

    def setState(self, state):
        self.state = state


def distnace(vec1, vec2):
    return math.sqrt((vec2[0]-vec1[0])**2+(vec2[1]-vec1[1])**2)


def copy(vec):
    return [vec[0], vec[1]]


class Car:
    def __init__(self, big_road, road_index):
        self.big_road = big_road  # 4
        self.road_index = road_index  # 3
        self.pos = copy(start_road_pos[big_road][road_index])
        self.vel = speed_list[big_road][road_index]  # (x, y)
        self.isCrossed = False
        self.overlaped = False
        if self.road_index == 1:
            self.velList = speed_list[big_road][road_index]
            self.vel = self.velList[0]

    def isOverWindow(self):
        if self.pos[0] > screen_width:
            return True
        elif self.pos[0] < 0:
            return True
        if self.pos[1] > screen_height:
            return True
        elif self.pos[1] < 0:
            return True
        return False

    def isStopTraffic(self, big_road, road_index) -> bool:
        if road_index == 2 or self.isCrossed == True:
            return False  # 우회전이면 프리패스
        if trafficList[big_road].state == 0:
            return True  # stop
        elif trafficList[big_road].state == 2 and road_index == 1:  # 좌회전 & 직진
            return True
        elif trafficList[big_road].state == 1 and road_index == 0:  # 좌회전 & 직진
            return True
        self.isCrossed = True
        return False

    def leftOperateInStop(self):
        self.vel = self.velList[1]
        if self.big_road == 0 and self.pos[1] >= stop_road_pos[3][1]:
            self.vel = self.velList[2]
        elif self.big_road == 1 and self.pos[1] <= stop_road_pos[2][1]:
            self.vel = self.velList[2]
        elif self.big_road == 2 and self.pos[0] >= stop_road_pos[0][0]:
            self.vel = self.velList[2]
        elif self.big_road == 3 and self.pos[0] <= stop_road_pos[1][0]:
            self.vel = self.velList[2]

    def isOverlap(self):
        after = [self.pos[0]+self.vel[0], self.pos[1]+self.vel[1]]
        for i in renderList:
            if i != self and i.big_road == self.big_road and i.road_index == self.road_index:
                if distnace(after, i.pos) < 60:
                    if i.big_road == 0:
                        if self.pos[1] < i.pos[1]:
                            return True
                    elif i.big_road == 1:
                        if self.pos[1] > i.pos[1]:
                            return True
                    elif i.big_road == 2:
                        if self.pos[0] < i.pos[0]:
                            return True
                    elif i.big_road == 3:
                        if self.pos[0] > i.pos[0]:
                            return True
        return False

    def move(self):
        isStop = False
        isTraffic = False
        stop = stop_road_pos[self.big_road]
        if self.big_road == 0 and self.pos[1] >= stop[1]:
            isStop = self.isStopTraffic(self.big_road, self.road_index)
            isTraffic = True
        elif self.big_road == 1 and self.pos[1] <= stop[1]:
            isStop = self.isStopTraffic(self.big_road, self.road_index)
            isTraffic = True
        elif self.big_road == 2 and self.pos[0] >= stop[0]:
            isStop = self.isStopTraffic(self.big_road, self.road_index)
            isTraffic = True
        elif self.big_road == 3 and self.pos[0] <= stop[0]:
            isStop = self.isStopTraffic(self.big_road, self.road_index)
            isTraffic = True

        if isTraffic and self.road_index == 1:
            self.leftOperateInStop()
        if not isStop:
            self.overlaped = self.isOverlap()
            if not self.overlaped:
                self.pos[0] += self.vel[0]
                self.pos[1] += self.vel[1]

    def draw(self):
        # rectValue = (self.pos[0],self.pos[1],self.pos[0]+CarSize,self.pos[1]+CarSize)
        # pygame.draw.rect(background,(255,0,0), rectValue)
        car_object = pygame.Rect(self.pos[0], self.pos[1], car_w, car_h)
        background.blit(car_img, car_object)

last_tindex=-1
freeTraffTick=0
def operateTarffic():
    global last_tindex, freeTraffTick
    if isMoving():
        freeTraffTick=0
        return
    else:
        freeTraffTick+=1

    if freeTraffTick < 1200 :
        return
    data = {}
    for i in renderList:
        n = '0'
        if i.big_road == 2 or i.big_road == 3:
            n = '1'
        d = distnace([425, 425], i.pos)
        try:
            data[n]['count'] -= d
        except:
            data[n] = {'count': -d, 'road': [0, 0, 0]}
        data[n]['road'][i.road_index] -= d
    selectN = '0'
    if data['0']['count'] > data['1']['count']:
        selectN = '1'
    selected = data[selectN]['road'].index(min(data[selectN]['road']))
    tindex = -1
    if selectN == '0':
        if selected == 0:
            tindex = 0
        else:
            tindex = 1
    else:
        if selected == 0:
            tindex = 2
        else:
            tindex = 3
    [trafficList[i].setState(trafficSystemList[tindex][i]) for i in range(4)]
    if last_tindex!=tindex:
        direction=['수직', '수평'][int(selectN)]
        traff=["좌회전","직진"][tindex==0 or tindex==2]
        print(f'[Traffic] >> {direction}방향\t{traff}\t신호로 변경되었습니다.')
    last_tindex=tindex


def isMoving():
    for i in renderList:
        if 290<i.pos[0] and 290<i.pos[1] and 630>i.pos[0] and 630>i.pos[1]:
            return True
    return False

# Main
renderList = [Car(r.randint(0, 3), r.randint(0, 2)) for _ in range(20)]

trafficList = [
    TrafficLight(181, 236),  # 상
    TrafficLight(662, 664),  # 하
    TrafficLight(185, 664),  # 좌
    TrafficLight(662, 240),  # 우
]

play = True
tick = 0
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    background.blit(image_bg, (0, 0))

    for i in trafficList:
        i.draw()

    outIndexList = []
    for i in range(len(renderList)):
        renderList[i].draw()
        renderList[i].move()
        if renderList[i].isOverWindow():
            outIndexList.append(i)
    outIndexList.reverse()
    for i in outIndexList:
        renderList.pop(i)
    [renderList.append(Car(r.randint(0, 3), r.randint(0, 2)))
     for _ in outIndexList]
    operateTarffic()
    pygame.display.update()

pygame.quit()

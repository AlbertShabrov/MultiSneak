import pygame
import random
import re
from network import Network

#colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#network settings
food_list = [-1, 0]
second_snake_list = []
second_snake_head = []
net = Network()
#screen settings
WIDTH = 800  # ширина игрового окна
HEIGHT = 600 # высота игрового окна
FPS = 10 # частота кадров в секунду
#coords
snake_block=10  #Один шаг змейки в размерах экрана
x1 = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
y1 = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0

snake_list = []
length_of_snake = 1
direction = None
x1_change = 0
y1_change = 0
#coords for food
foodx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
foody = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0

def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_block, snake_block])

def draw_another_food(snake_block, food_list):
        pygame.draw.rect(screen, RED, [food_list[0], food_list[1], snake_block, snake_block])

def send_data():
    food_coords = [foodx, foody]
    snake_list_copy = list(snake_list)
    snake_list_copy.append(food_coords)
    data = str(net.id) + ":" + str(snake_list_copy)
    reply = net.send(data)
    return reply

def convert_data_to_list(data):
    second_list = []
    food_coords = []
    new_data = data[1: -1]
    new_reply = list(re.findall('\[([^]]+)', new_data))
    for item in new_reply:
        result = item.split(',')
        new_results = [float(item) for item in result]
        second_list.append(new_results)
    if len(second_list) > 1:
        food_coords = second_list[-1]
        second_list.pop()
    else:
        food_coords = [-1 ,0]
    return [second_list, food_coords]

def parse_data(data):
    try:
        d = str(data.split(":")[1])
        return d
    except:
        return 0, 0

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MultiSneak")
clock = pygame.time.Clock()
bg = pygame.image.load("sand.jpg").convert()
font_style = pygame.font.SysFont(None, 50)

while(True):
    clock.tick(FPS)                     #Указываем частоту обновления экрана
    for event in pygame.event.get():    #Ивент на закрытие окна игры
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not direction == "RIGHT":
                direction = "LEFT"
                x1_change = -snake_block
                y1_change = 0
            elif event.key == pygame.K_RIGHT and not direction == "LEFT":
                direction = "RIGHT"
                x1_change = snake_block
                y1_change = 0
            elif event.key == pygame.K_UP and not direction == "DOWN":
                direction = "UP"
                y1_change = -snake_block
                x1_change = 0
            elif event.key == pygame.K_DOWN and not direction == "UP":
                direction = "DOWN"
                y1_change = snake_block
                x1_change = 0

    if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0: #Конец игры при выходе за пределы экрана
        snake_list.clear()
        snake_head.clear()
        length_of_snake = 1
        x1 = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
        y1 = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0

    x1 += x1_change
    y1 += y1_change

    snake_head = []
    snake_head.append(x1)
    snake_head.append(y1)
    snake_list.append(snake_head)
    if len(snake_list) > length_of_snake:
        del snake_list[0]

    for x in snake_list[:-1]:
        if x == snake_head:
            snake_list.clear()
            snake_head.clear()
            length_of_snake = 1
            x1 = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
            y1 = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0

    for x in second_snake_list:
        if x == snake_head:
            snake_list.clear()
            snake_head.clear()
            length_of_snake = 1
            x1 = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
            y1 = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0

    second_snake_list, food_list = convert_data_to_list(parse_data(send_data()))
    try:
        second_snake_head = second_snake_list[0]
        if second_snake_head[0] == foodx and second_snake_head[1] == foody:
            foodx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0
            length_of_snake += 1
    except IndexError:
        pass

    if (x1 == foodx and y1 == foody) or (x1 == food_list[0] and y1 == food_list[1]):
        foodx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0
        length_of_snake += 1


    #Отоброжаем все
    screen.blit(bg, (0, 0))          #background
    draw_snake(snake_block, snake_list)
    pygame.draw.rect(screen, RED, [foodx, foody, snake_block, snake_block])
    draw_another_food(snake_block, food_list)
    draw_snake(snake_block, second_snake_list)
    pygame.display.flip()
pygame.quit()

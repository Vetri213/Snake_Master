import pygame
import random
import cv2
import time
import os
import HandTrackingModule as htm
import direction as dir
import sys

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 600
dis_height = 400

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Master')

clock = pygame.time.Clock()

snake_block = 10
food_block = 20
snake_speed = 10

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])
    high_score(score)
    return score

file = open("highscore.txt","r")

old_highscore = int(file.read())
file.close()

highscore = old_highscore

def high_score(score):
    global old_highscore
    global highscore
    # Use highscore.txt to add the highscore - update it
    if (score > highscore):
        highscore = score
    value1 = score_font.render("High Score: " + str(highscore), True, yellow)
    dis.blit(value1, [250, 0])

num = random.randint(1, 5)
if num == 1:
    color1 = "blue"
elif num == 2:
    color1 = "red"
elif num == 3:
    color1 = "black"
elif num == 4:
    color1 = "green"
else:
    color1 = "purple"

def our_snake(snake_block, snake_list):

    for i in range(len(snake_list)-1):
        pygame.draw.rect(dis, color1, [snake_list[i][0], snake_list[i][1], snake_block, snake_block])
    pygame.draw.rect(dis, color1, [snake_list[-1][0], snake_list[-1][1], snake_block, snake_block])

    # Random colour

    """for i in range(len(snake_list)):
        num = random.randint(1, 5)
        if num == 1:
            color1 = "blue"
        elif num == 2:
            color1 = "red"
        elif num == 3:
            color1 = "black"
        elif num == 4:
            color1 = "green"
        else:
            color1 = "purple"
        pygame.draw.rect(dis, color1, [snake_list[i][0], snake_list[i][1], snake_block, snake_block])"""


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def gameLoop():
    opp = 0
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    #last_direction = None
    direction = [None,None]
    head =[None,None]
    second = [None,None]
    while not game_over:
        last_direction = direction[0]

        success, img = cap.read()

        #if direction[0] != None:
            #last_direction = direction[0]
        #print(last_direction)

        direction = dir.pose(img)
        # state = dir.count(img)
        # if state == "exit":
        #     game_close = True
        #print (direction[0])
        # if direction[0] != None:
        # Hello

        opp_direction = None

        # if last_direction == "right":
        #     opp_direction = "left"
        # elif last_direction == "left":
        #     opp_direction = "right"
        # elif last_direction == "down":
        #     opp_direction = "up"
        # elif last_direction == "up":
        #     opp_direction = "down"

        if (head[0] and second[0]):
            if (head[0] == (second[0]+10)):
                #Right
                print("Right")
                opp_direction = "left"
            elif (head[0] == (second[0]-10)):
                # Left
                print("Left")
                opp_direction = "right"
            elif (head[1] == (second[1]-10)):
                # Up
                print("Up")
                opp_direction = "down"
            elif (head[1] == (second[1]+10)):
                # Down
                print("Down")
                opp_direction = "up"
        # #print(opp_direction)
        # if opp_direction == direction:
        #     print("Stop")
        #     direction = last_direction
        #     pass
        #
        if (direction[0] == opp_direction):
            pass
        elif direction[0] == "left":
            x1_change = -snake_block
            y1_change = 0
        elif direction[0] == "right":
            x1_change = snake_block
            y1_change = 0
        elif direction[0] == "up":
            y1_change = -snake_block
            x1_change = 0
        elif direction[0] == "down":
            y1_change = snake_block
            x1_change = 0

        if x1 >= dis_width:
            x1 = 0
        if x1 < 0:
            x1 = dis_width
        if y1 >= dis_height:
            y1 = 0
        if y1 < 0:
            y1 = dis_height

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, food_block, food_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        head = snake_Head
        try:
            second = snake_List[-2]
        except:
            pass
        #print("Snake Head:",head,"Snake Second:",second)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        high_score(Your_score(Length_of_snake - 1))

        pygame.display.update()

        if (x1 < (foodx + food_block) and x1 >= foodx) and (y1 < (foody + food_block) and y1 >= foody):
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

        while game_close == True:
            success, img = cap.read()
            dis.fill(blue)
            message("Game Over! 3 up to retry or 4 up to quit", red)
            Your_score(Length_of_snake - 1)


            pygame.display.update()

            state = dir.count(img)
            if state == "quit":
                if (old_highscore < Length_of_snake - 1):
                    file = open("highscore.txt", "w")
                    file.write(str(Length_of_snake-1))
                    file.close()
                game_over = True
                game_close = False
            elif state == "continue":
                gameLoop()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
    pygame.quit()
    quit()







gameLoop()
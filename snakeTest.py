#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-06-08 20:54:50
# @Author  : Kelly Hwong (you@example.org)
# @Link    : http://example.org
# @Version : $Id$


import random
import sys
import time
import pygame
from pygame.locals import *

from snake_ai import SnakeAI

# 游戏常量，世界大小
FPS = 5  # 屏幕刷新率（在这里相当于贪吃蛇的速度）
WINDOWWIDTH = 640  # 屏幕宽度
WINDOWHEIGHT = 480  # 屏幕高度
CELLSIZE = 20  # 小方格的大小

# 断言，屏幕的宽和高必须能被方块大小整除
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."

# 横向和纵向的方格数
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

WORLD_WIDTH = CELLWIDTH
WORLD_HEIGHT = CELLHEIGHT

GAME_MODE = "GAME_MODE"
AI_MODE = "AI_MODE"

# 定义几个常用的颜色
# R G B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

# 定义贪吃蛇的动作
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


class Snake(object):
    """Implement a snake algorithm level class

    Please firstly init a cells list for the snake
    For printing/visualizing the snake, write a interface

    Note:
        NULL

    Args:
        dim (list): Dimensions of the snake world.
        cells (list): Coordinates of the snake.

    Attributes:
        msg (str): Human readable string describing the exception.
        code (int): Exception error code.

    """

    def __init__(self, dim, cells, direction=RIGHT):
        self.dim = dim
        self.cells = cells
        self.direction = direction

    def eat_apple(self, apple) -> bool:
        if self.cells[0][0] == apple[0] and self.cells[0][1] == apple[1]:
            # 不移除蛇的最后一个尾巴格
            return True
        else:
            del self.cells[-1]  # 移除蛇的最后一个尾巴格
            return False

    def move(self):
        # 根据方向，添加一个新的蛇头，以这种方式来移动贪吃蛇
        if self.direction == UP:
            new_head = (self.cells[0][0], self.cells[0][1] - 1)
        elif self.direction == DOWN:
            new_head = (self.cells[0][0], self.cells[0][1] + 1)
        elif self.direction == LEFT:
            new_head = (self.cells[0][0] - 1, self.cells[0][1])
        elif self.direction == RIGHT:
            new_head = (self.cells[0][0] + 1, self.cells[0][1])
        # 插入新的蛇头在数组的最前面
        self.cells.insert(0, new_head)

    def alive(self):
        # 检查贪吃蛇是否撞到撞到边界
        if self.cells[0][0] == -1 or self.cells[0][0] == CELLWIDTH or self.cells[0][1] == -1 or self.cells[0][1] == CELLHEIGHT:
            return  # game over
        # 检查贪吃蛇是否撞到自己
        for cell in self.cells[1:]:
            if cell[0] == self.cells[0][0] and cell[1] == self.cells[0][1]:
                return  # game over


class SnakeGame(object):
    """Implement a snake pygame GUI level class

    Please firstly init a cells list for the snake
    For printing/visualizing the snake, write a interface

    Note:
        NULL

    Args:
        dim (list): Dimensions of the snake world.
        cells (list): Coordinates of the snake.

    Attributes:
        msg (str): Human readable string describing the exception.
        code (int): Exception error code.

    """

    def __init__(self, snake, mode=GAME_MODE, ai=None):
        self.snake = snake
        self.mode = mode
        self.ai = ai
    '''
    def next_direction(self):
        if self.mode == AI_MODE:
            # 有没有AI
            if not self.ai:
                print("请接入蛇皮AI")
                sys.quit()
                # raise
            direction = self.ai.predict()
        else:
            direction = monitor_key()
        return direction

    def monitor_key(self):

        for event in pygame.event.get():  # 事件处理
            if event.type == QUIT:  # 退出事件
                self.terminate()
            elif event.type == KEYDOWN:  # 按键事件
                # 如果按下的是左键或a键，且当前的方向不是向右，就改变方向，以此类推
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    self.terminate()

    # 退出
    def terminate(self):
        pygame.quit()
        sys.exit()
    '''

# 绘制提示消息


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

# 检查按键是否有按键事件


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

# 显示开始画面


def showStartScreen():
    DISPLAYSURF.fill(BGCOLOR)
    titleFont = pygame.font.Font('PAPYRUS.ttf', 100)
    titleSurf = titleFont.render('Wormy!', True, GREEN)
    titleRect = titleSurf.get_rect()
    titleRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    DISPLAYSURF.blit(titleSurf, titleRect)
    drawPressKeyMsg()
    pygame.display.update()
    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return


# 随机生成一个坐标位置


def getRandomLocation():
    return (random.randint(0, CELLWIDTH - 1), random.randint(0, CELLHEIGHT - 1))


# 显示游戏结束画面


def showGameOverScreen():
    gameOverFont = pygame.font.Font('PAPYRUS.ttf', 50)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2-gameRect.height-10)
    overRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()  # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return

# 绘制分数


def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


# 根据 cells 数组绘制贪吃蛇
def drawWorm(cells):
    for coord in cells:
        x = coord[0] * CELLSIZE
        y = coord[1] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(
            x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


# 根据 coord 绘制 apple
def drawApple(apple):
    x = apple[0] * CELLSIZE
    y = apple[1] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)

# 绘制所有的方格


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


def runGame(snake: Snake, apple=(0, 0)):
    while True:  # 游戏主循环
        for event in pygame.event.get():  # 事件处理
            if event.type == QUIT:  # 退出事件
                terminate()
            elif event.type == KEYDOWN:  # 按键事件
                # 如果按下的是左键或a键，且当前的方向不是向右，就改变方向，以此类推
                if (event.key == K_LEFT or event.key == K_a) and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and snake.direction != LEFT:
                    snake.direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and snake.direction != DOWN:
                    snake.direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        snake.alive()
        # 检查贪吃蛇是否吃到apple
        if snake.eat_apple(apple):
            apple = getRandomLocation()  # 重新随机生成一个apple
        snake.move()

        # 绘制背景
        DISPLAYSURF.fill(BGCOLOR)
        # 绘制所有的方格
        drawGrid()
        # 绘制贪吃蛇
        drawWorm(snake.cells)
        # 绘制apple
        drawApple(apple)
        # 绘制分数（分数为贪吃蛇数组当前的长度-3）
        drawScore(len(snake.cells) - 3)
        # 更新屏幕
        pygame.display.update()
        # 设置帧率
        FPSCLOCK.tick(FPS)


def main():
    pygame.init()  # 初始化pygame

    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    # 以这个点为起点，建立一个长度为3格的贪吃蛇（数组）
    wormCoords = [(startx, starty),
                  (startx - 1, starty),
                  (startx - 2, starty)]
    snake = Snake(dim=(WORLD_WIDTH, WORLD_HEIGHT),
                  cells=wormCoords, direction=RIGHT)
    # ai = SnakeAI(snake=snake)
    snakeGame = SnakeGame(snake=snake, mode=GAME_MODE)

    apple = getRandomLocation()

    # 定义全局变量
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    FPSCLOCK = pygame.time.Clock()  # 获得pygame时钟
    DISPLAYSURF = pygame.display.set_mode(
        (WINDOWWIDTH, WINDOWHEIGHT))  # 设置屏幕宽高
    BASICFONT = pygame.font.Font('PAPYRUS.ttf', 18)  # BASICFONT
    pygame.display.set_caption('Greedy Snake AI')  # 设置窗口的标题

    showStartScreen()  # 显示开始画面

    while True:
        # 这里一直循环于开始游戏和显示游戏结束画面之间，
        # 运行游戏里有一个循环，显示游戏结束画面也有一个循环
        # 两个循环都有相应的return，这样就可以达到切换这两个模块的效果
        # 你不会多线程？ by
        runGame(snake=snake, apple=apple)  # 运行游戏
        showGameOverScreen()  # 显示游戏结束画面

# 退出


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()

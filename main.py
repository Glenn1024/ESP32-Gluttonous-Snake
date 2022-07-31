from machine import Pin, SPI
from game import Game
from tools import DoubleNode, DoubleLinkedList
import random, time

class Snake:
    UP = -1
    DOWN = 1
    LEFT = -2
    RIGHT = 2

    def __init__(self, head, length, width, h_color, b_color, g):
        self.g = g      # 游戏基础对象
        
        self.length = length        ## 设置蛇的身体长度
        self.width = width      ## 设置蛇的身体宽度
        self.h_color = h_color      ## 设置蛇的头部颜色
        self.b_color = b_color      ## 设置蛇的身体颜色
        self.direction = Snake.RIGHT
        
        self.snake = DoubleLinkedList()       ## 保存蛇的身体
        self.snake.add(DoubleNode(head))
        
        node = self.snake.head
        for n in range(length):       ## 生成蛇的身体 并 进行绘制
            node = DoubleNode((node.val[0]-self.width, node.val[1]), prev=node)
            self.snake.append(node)
            self.g.st7735.fill_rect(node.val[0], node.val[1], self.width, self.width, self.b_color)
        self.g.st7735.fill_rect(self.snake.head.val[0], self.snake.head.val[1], self.width, self.width, self.h_color)
        self.show()

    def change_direction(self, event):
        if event:
            if event == "UP":
                direction = Snake.UP
            elif event == "DOWN":
                direction = Snake.DOWN
            elif event == "LEFT":
                direction = Snake.LEFT
            elif event == "RIGHT":
                direction = Snake.RIGHT
            if direction+self.direction != 0:
                self.direction = direction

    def move(self):
        self.g.st7735.fill_rect(self.snake.head.val[0], self.snake.head.val[1], self.width, self.width, self.b_color)
        
        if self.direction == Snake.UP:
            node = DoubleNode((self.snake.head.val[0], self.snake.head.val[1]-self.width))
        elif self.direction == Snake.DOWN:
            node = DoubleNode((self.snake.head.val[0], self.snake.head.val[1]+self.width))
        elif self.direction == Snake.LEFT:
            node = DoubleNode((self.snake.head.val[0]-self.width, self.snake.head.val[1]))
        elif self.direction == Snake.RIGHT:
            node = DoubleNode((self.snake.head.val[0]+self.width, self.snake.head.val[1]))
        
        if node.val != self.snake.head.next.val:
            tail = self.snake.pop()
            self.g.st7735.fill_rect(tail.val[0], tail.val[1], self.width, self.width, self.g.bg_color)
            self.snake.add(node)
            self.g.st7735.fill_rect(self.snake.head.val[0], self.snake.head.val[1], self.width, self.width, self.h_color)
            self.show()
        
        return self.die(self.snake.head)

    def die(self, node):
        if self.snake.head.val[0]==0 or self.snake.head.val[1]==self.g.screen_size[1]-self.g.size[1] or self.snake.head.val[0]==self.g.size[0] or self.snake.head.val[1]==self.g.screen_size[1]:
            return True
        
        node = self.snake.tail
        for n in range(self.length-3):
            if self.snake.head.val == node.val:
                return True
            node = node.prev
        
        return False
    
    def eat(self, snack):
        if self.snake.head.val == snack.position:
            self.length+=1
            node = DoubleNode((self.snake.tail.val[0]-self.width, self.snake.tail.val[1]), prev=self.snake.tail)
            self.snake.append(node)
            self.g.st7735.fill_rect(node.val[0], node.val[1], self.width, self.width, self.b_color)
            self.show()
            return True
        return False

    def show(self):
        self.g.st7735.show()

class Snack:
    is_exist = False
    def __init__(self, position, width, color, g):
        self.g = g
        self.position = position
        self.color = color
        self.width = width
        
        self.show()

    def show(self):
        self.g.st7735.fill_rect(self.position[0], self.position[1], self.width, self.width, self.color)
        self.g.st7735.show()


def main():
    Pin(18, Pin.OUT).value(1)
    spi=SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(15), mosi=Pin(0))
    game=Game((128,112), 0xFFF)
    game.set_screen(spi,(128, 128),dc=Pin(16),cs=Pin(17),rst=Pin(4),rot=2,bgr=0)
    game.set_bar()
    keys = {
        "UP": Pin(13, Pin.IN, Pin.PULL_DOWN),
        "DOWN": Pin(12, Pin.IN, Pin.PULL_DOWN),
        "LEFT": Pin(14, Pin.IN, Pin.PULL_DOWN),
        "RIGHT": Pin(27, Pin.IN, Pin.PULL_DOWN)
    }
    game.set_key(keys)
    while True:
        game.restart()
        width = 4
        length = 4
        snake = Snake((40, 64), length, width, 0x0F0, 0x000, game)
        while True:
            game.st7735.text("score: {}".format(snake.length-length-1), (game.screen_size[1]-game.size[1]-8)//2, (game.screen_size[1]-game.size[1]-8)//2, game.bg_color)
            game.st7735.text("score: {}".format(snake.length-length), (game.screen_size[1]-game.size[1]-8)//2, (game.screen_size[1]-game.size[1]-8)//2, 0x000)
            if not Snack.is_exist:
                position = (
                    random.randint(width, game.size[0]//width-width)*width,
                    random.randint((game.screen_size[1]-game.size[1])//width+width, game.size[1]//width-width)*width
                )
                snack = Snack(position, width, 0xF00, game)
                Snack.is_exist = True
            time.sleep_ms(30)
            event = game.get_event()
            snake.change_direction(event)
            snack.show()
            if snake.eat(snack):
                Snack.is_exist = False
            if snake.move():
                Snack.is_exist = False
                break
            time.sleep_ms(30)

if __name__ == "__main__":
    main()

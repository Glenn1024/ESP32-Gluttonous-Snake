'''
Auther: LUWic
Date: 2022-7-17
Introduce: 基于st7735的游戏库
'''

import st7735, _thread

class Game:
    def __init__(self, size, bg_color):
        self.size = size
        self.screen_size = size
        self.bg_color = bg_color
        self.event_list = []
        self.keys = {}

    def set_screen(self, spi, size, dc, rst, cs, rot=0, bgr=0):
        self.screen_size = size
        self.st7735 = st7735.ST7735(size[0], size[1], spi, dc, rst, cs, rot=rot, bgr=bgr)
        self.st7735.fill(0xFFF)
        self.st7735.show()

    def set_key(self, keys):
        '''
            keys: {"key_name", Pin(2, Pin.IN)}
        '''
        self.keys = keys
        _thread.start_new_thread(self.add_event, ())

    def set_bar(self):
        self.st7735.line(0, self.screen_size[1]-self.size[1], self.screen_size[0], self.screen_size[1]-self.size[1], 0x000)
        self.st7735.show()

    def restart(self):
        self.st7735.fill(0xFFF)
        self.st7735.show()
        self.set_bar()

    def get_event(self):
        if len(self.event_list):
            return self.event_list.pop(0)
        return None
    
    def add_event(self):
        _keys = {}
        for k in self.keys.keys():
            _keys[k]=0
        while True:
            for k,v in self.keys.items():
                if not v.value() and _keys[k]:
                    self.event_list.append(k)
                    _keys[k] = 0
                elif v.value():
                    _keys[k] = 1
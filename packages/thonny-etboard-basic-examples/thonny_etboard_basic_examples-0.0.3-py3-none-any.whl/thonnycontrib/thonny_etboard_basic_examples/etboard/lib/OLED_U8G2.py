from machine import Pin, SoftI2C
from ETboard.lib import ssd1306
from ETboard.lib.pin_define import *
from machine import ADC


class oled_u8g2:
    def __init__(self):
        i2c = SoftI2C(scl=Pin(22), sda=Pin(21)) # oled 통신핀 기능 설정
        oled_width = 128 # oled 너비
        oled_height = 64 # oled 높이
        self.oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
        
    def __del__(self):
        pass
    
    def clear(self):
        self.oled.fill(0)
    
    def setLine(self, lineNum, text):
        yNum = (lineNum - 1) * 8
        self.oled.text(text, 0, yNum)
    
    def display(self):
        self.oled.show()

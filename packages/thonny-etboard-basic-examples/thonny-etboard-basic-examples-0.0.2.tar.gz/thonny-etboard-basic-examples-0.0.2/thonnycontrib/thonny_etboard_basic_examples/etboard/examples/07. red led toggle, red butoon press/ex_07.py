# ********************************************************************************
# FileName : ex_07
# Description : 빨간 버튼이 눌리면 빨간 LED를 켜고
#               다시 버튼이 눌리면 빨간 LED를 끄는 예제
# Author : 이인정
# Created Date : 2021.05.31
# Reference :
# Modified : 2021.06.01 : LIJ : 헤더수정
# ********************************************************************************

# import
from ETboard.lib.pin_define import *
from machine import Pin
import time

# global definition
state = LOW                # LED 상태
reading = HIGH             # 버튼 상태
previous = LOW             # 버튼 이전 상태
_time = 0                  # LED가 ON/OFF 토글된 마지막 시간
debounce = 100             # debounce(눌린시간) 시간 설정


# setup
PinD2 = Pin(D2, Pin.OUT)   # D2를 LED 출력모드 설정하기
Pin6 = Pin(D6, Pin.IN)     # D6을 버튼 입력모드 설정하기


# main loop
while True:
    reading = Pin6.value()  # Button 상태 읽기
    
    # 버튼이 눌려졌고 버튼 눌림 시간이 debounce(설정해둔 눌린시간) 시간보다 크면 실행
    if reading == HIGH and previous == LOW and time.ticks_ms() - _time > debounce:
        if state == HIGH:
            state = LOW
        else:
            state = HIGH
        
        _time = time.ticks_ms()
    
    PinD2.value(state)
    
    previous = reading

# ┌───────────────────────────────────────────┐
# │                                           │
# │(주)한국공학기술연구원 http://et.ketri.re.kr│
# │                                           │
# └───────────────────────────────────────────┘

# ********************************************************************************
# FileName : ex_01
# Description : 빨간 LED를 2회 켜고 끄는 예제
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
count = 0                  # LED를 2회만 켜고 끄기를 위한 변수


# setup
PinD2 = Pin(D2, Pin.OUT)   # D2를 LED 출력모드 설정


# main loop
while count < 1:
    time.sleep(2)          # 2초 기다리기
    PinD2.value(HIGH)      # LED 켜기
    time.sleep(2)          # 2초 기다리기
    PinD2.value(LOW)       # LED 끄기

    time.sleep(2)          # 2초 기다리기
    PinD2.value(HIGH)      # LED 켜기
    time.sleep(2)          # 2초 기다리기
    PinD2.value(LOW)       # LED 끄기

    count = 1              # 프로그램을 종료시키기 위해 count 변수값 변경

# ┌───────────────────────────────────────────┐
# │                                           │
# │(주)한국공학기술연구원 http://et.ketri.re.kr│
# │                                           │
# └───────────────────────────────────────────┘

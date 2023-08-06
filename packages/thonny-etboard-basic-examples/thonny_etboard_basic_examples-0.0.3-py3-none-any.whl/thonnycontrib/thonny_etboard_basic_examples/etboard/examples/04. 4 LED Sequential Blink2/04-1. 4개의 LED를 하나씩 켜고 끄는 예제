# ********************************************************************************
# FileName : ex_04
# Description : 4개의 LED를 하나씩 켜고 끄는 예제
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
count = 0                 # 4개의 LED를 1회만 켜고 끄기 위한 변수


# setup
PinD2 = Pin(D2, Pin.OUT)  # D2를 LED 출력모드 설정하기
PinD3 = Pin(D3, Pin.OUT)  # D3를 LED 출력모드 설정하기
PinD4 = Pin(D4, Pin.OUT)  # D4를 LED 출력모드 설정하기
PinD5 = Pin(D5, Pin.OUT)  # D5를 LED 출력모드 설정하기


# main loop
while count < 1:
    time.sleep(1)         # 1초 기다리기
    PinD2.value(HIGH)     # 빨강 LED 켜기
    time.sleep(1)         # 1초 기다리기
    PinD2.value(LOW)      # 빨강 LED 끄기
    
    time.sleep(1)         # 1초 기다리기
    PinD4.value(HIGH)     # 초록 LED 켜기
    time.sleep(1)         # 1초 기다리기
    PinD4.value(LOW)      # 초록 LED 끄기
    
    time.sleep(1)         # 1초 기다리기
    PinD5.value(HIGH)     # 노랑 LED 켜기
    time.sleep(1)         # 1초 기다리기
    PinD5.value(LOW)      # 노랑 LED 끄기
      
    time.sleep(1)         # 1초 기다리기
    PinD3.value(HIGH)     # 파랑 LED 켜기
    time.sleep(1)         # 1초 기다리기
    PinD3.value(LOW)      # 파랑 LED 끄기
    
    count = 1             # LED를 제어하지 않기 위해 count 변수를 1로 변경
  
# ┌───────────────────────────────────────────┐
# │                                           │
# │(주)한국공학기술연구원 http://et.ketri.re.kr│
# │                                           │
# └───────────────────────────────────────────┘

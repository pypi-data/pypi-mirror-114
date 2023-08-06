# ********************************************************************************
# FileName : ex_08
# Description : 버튼을 누르면 버튼과 같은색의 LED를 켜는 예제
# Author : 이인정
# Created Date : 2021.05.31
# Reference :
# Modified : 2021.06.01 : LIJ : 헤더수정
# ********************************************************************************

# import
from ETboard.lib.pin_define import *
from machine import Pin


# setup
# Button 입력 모드 설정
Pin6 = Pin(D6, Pin.IN)       # 빨강색 버튼 입력모드 설정하기
Pin7 = Pin(D7, Pin.IN)       # 파랑색 버튼 입력모드 설정하기
Pin8 = Pin(D8, Pin.IN)       # 초록색 버튼 입력모드 설정하기
Pin9 = Pin(D9, Pin.IN)       # 노랑색 버튼 입력모드 설정하기

# LED 출력 모드 설정
Pin2 = Pin(D2, Pin.OUT)      # 빨강색 LED 출력모드 설정하기
Pin3 = Pin(D3, Pin.OUT)      # 파랑색 LED 출력모드 설정하기
Pin4 = Pin(D4, Pin.OUT)      # 초록색 LED 출력모드 설정하기
Pin5 = Pin(D5, Pin.OUT)      # 노랑색 LED 출력모드 설정하기


# main loop
while True:
    if Pin6.value() == LOW:  # 빨강 버튼이 눌리면 빨강 LED 켜기
        Pin2.value(HIGH)
    
    if Pin7.value() == LOW:  # 파랑 버튼이 눌리면 파랑 LED 켜기
        Pin3.value(HIGH)
    
    if Pin8.value() == LOW:  # 초록 버튼이 눌리면 초록 LED 켜기
        Pin4.value(HIGH)
    
    if Pin9.value() == LOW:  # 노랑 버튼이 눌리면 노랑 LED 켜기
        Pin5.value(HIGH)
    
# ┌───────────────────────────────────────────┐
# │                                           │
# │(주)한국공학기술연구원 http://et.ketri.re.kr│
# │                                           │
# └───────────────────────────────────────────┘

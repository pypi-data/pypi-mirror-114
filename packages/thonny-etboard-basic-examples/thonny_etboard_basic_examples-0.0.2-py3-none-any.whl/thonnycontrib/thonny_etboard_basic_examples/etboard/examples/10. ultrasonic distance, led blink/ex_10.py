# ********************************************************************************
# FileName : ex_10
# Description : 초음파센서를 이용해 거리를 측정하는 예제
#               거리 값에 따라서 LED가 점등함
# Author : 이인정
# Created Date : 2021.05.31
# Reference :
# Modified : 2021.06.01 : LIJ : 헤더수정
# ********************************************************************************

# import
from ETboard.lib.pin_define import *
from machine import Pin, time_pulse_us
import time

# global definition
trigPin = Pin(D9, Pin.OUT)  # 초음파 송신부
echoPin = Pin(D8, Pin.IN)   # 초음파 수신부
usw_threshold_1 = 10        # 초음파센서 임계치_1
usw_threshold_2 = 20        # 초음파센서 임계치_2


# setup
# LED 출력모드 설정
Pin2 = Pin(D2, Pin.OUT)     # 빨강 LED 출력 모드 설정하기
Pin4 = Pin(D4, Pin.OUT)     # 초록 LED 출력 모드 설정하기
Pin5 = Pin(D5, Pin.OUT)     # 노랑 LED 출력 모드 설정하기


# main loop
while True:
    # 초음파 송신 후 수신부는 HIGH 상태로 대기
    trigPin.value(LOW)
    echoPin.value(LOW)
    time.sleep_ms(2)
    trigPin.value(HIGH)
    time.sleep_ms(10)
    trigPin.value(LOW)
    
    # echoPin 이 HIGH를 유지한 시간 저장
    duration = time_pulse_us(echoPin, HIGH)
    # HIGH 였을 때 시간(초음파 송수신 시간)을 기준으로 거리를 계산
    distance = ((340 * duration) / 10000) / 2
    
    # 초음파센서 값을 출력
    print(distance, " cm ")                        # 거리를 화면에 출력해줌
    time.sleep_ms(100)                             # 0.1초 대기
    
    # 초음파센서 값에 따라 LED 제어
    if distance < usw_threshold_1:                 # 거리가 usw_threshold_1 미만이면
        Pin2.value(HIGH)                           # 빨강색 LED 켜짐
    else:
        Pin2.value(LOW)                            # 빨강색 LED 꺼짐

    # usw_threshold_2 초과이면 usw_threshold_1 미만이면
    if (distance < usw_threshold_2) and (distance > usw_threshold_1):
        Pin5.value(HIGH)                           # 노랑색 LED 켜짐
    else:
        Pin5.value(LOW)                            # 노랑색 LED 꺼짐
        
    if distance > usw_threshold_2:                 # usw_threshold_1 미만이면
        Pin4.value(HIGH)                           # 초록색 LED 켜짐
    else:
        Pin4.value(LOW)                            # 초록색 LED 꺼짐
        
# ┌───────────────────────────────────────────┐
# │                                           │
# │(주)한국공학기술연구원 http://et.ketri.re.kr│
# │                                           │
# └───────────────────────────────────────────┘

# ********************************************************************************
# FileName : ex_09
# Description : OLED에 문자열을 출력하는 예제
#               조도 센서의 값에 따라서 다른 문자열이 출력됨
# Author : 이인정
# Created Date : 2021.05.31
# Reference :
# Modified : 2021.06.01 : LIJ : 헤더수정
# ********************************************************************************

# import
from ETboard.lib.OLED_U8G2 import *
from machine import ADC

# global definition
oled = oled_u8g2()
CDS_threshold_1 = 300                # 조도센서 임계치_1
CDS_threshold_2 = 100                # 조도센서 임계치_2


# setup
sensor = ADC(Pin(A1))                 # 조도센서
sensor.atten(ADC.ATTN_11DB)


# main loop
while True:
    CDS_Value = sensor.read() / 16
    print(" 조도 센서 : ", CDS_Value)
    print("---------------------")

    if CDS_Value > CDS_threshold_1:
        oled.clear()                  # oled 내용을 지우기
        oled.setLine(1, "^^")         # 1번째 줄에 ^^ 출력하기
        oled.setLine(2, "GOOD")       # 2번째 줄에 GOOD 출력하기
        oled.setLine(3, "MORNING")    # 3번째 줄에 MORNING 출력하기

    if CDS_Value < CDS_threshold_2:
        oled.clear()                  # oled 내용을 지우기
        oled.setLine(1, "******")     # 1번째 줄에 ****** 출력하기
        oled.setLine(2, "GOOD")       # 2번째 줄에 GOOD 출력하기
        oled.setLine(3, "NIGHT!")     # 3번째 줄에 NIGHT! 출력하기

    oled.display()                    # 저장된 내용을 oled에 보여줌

# ┌───────────────────────────────────────────┐
# │                                           │
# │(주)한국공학기술연구원 http://et.ketri.re.kr│
# │                                           │
# └───────────────────────────────────────────┘

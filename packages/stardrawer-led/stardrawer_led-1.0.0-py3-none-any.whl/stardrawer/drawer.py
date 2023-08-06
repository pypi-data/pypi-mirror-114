import numpy as np

def draw_star_square(length):
    # 파이썬 내장 range 사용해도 되지만 requirements.txt을 통한 의존 라이브러리 설치를 확인하기 위해 numpy 사용
    for i in  np.arange(length):
        print('*' * length)


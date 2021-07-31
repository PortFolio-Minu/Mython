import numpy as np
import matplotlib.pyplot as plt
import datetime
import random
import pymysql

# 0 보다 작으면 0으로 조정
def positive(val) :
    if val < 0 :
        return 0
    else :
        return val

# Random 값에 따라 Peak 시간 조정
def selectTime(time):
    if time == 0 :
        return 11
    elif time == 1 or time == 2:
        return 12
    elif time == 3 :
        return 18
    elif time == 4:
        return 19
    else :
        return 20


# MySQL Connection 연결
conn = pymysql.connect(host='localhost', port=3306, user='root', password='password',db='db', charset='utf8')

mycursor = conn.cursor()

current = datetime.datetime(2019,1,1)

yearadd = [0, 700, 1400]

cnt = 0

UpperBoundYear = 2021

while(True):
    if current.year > UpperBoundYear :
        break
    if ( cnt % 30 ) == 0:
        print(str(round(cnt*100 / (365*3),2))+"%, "+str(current))
    data = [0 for i in range(24)]

    # 년도별 가산값 및 일별 랜덤 감가산값
    randomadd = random.randrange(0,2000)
    randomadd2 = random.randrange(0,2000)

    # PeakTime을 랜덤으로 설정
    randomTime1 = random.randrange(0,3)
    randomTime2 = random.randrange(3,6)

    randPeak1 = selectTime(randomTime1)
    randPeak2 = selectTime(randomTime2)


    # Peak Time이 11~12시, 17 ~ 19시 두 구간이 있으므로 랜덤하게 선택
    a = np.random.triangular(0, randPeak1, 23, 4000  + yearadd[current.year - 2019] + randomadd)
    b = np.random.triangular(0, randPeak2, 23, 5500 + yearadd[current.year - 2019] + randomadd2)

    hist, bin_edges= np.histogram(a, bins=24, range=None, normed=None, weights=None, density=None)
    hist2, bin_edges2= np.histogram(b, bins=24, range=None, normed=None, weights=None, density=None)

    # 24시간 데이터 입력
    for i in range(24) :
        if i < 13 :
            data[i] = positive(hist[i] + hist2[i] + random.randrange(-30,30)) 
        elif i < 16:
            data[i] = positive(0.65*hist[i] + hist2[i] + random.randrange(-30,30))
        else :
            data[i] = positive(hist2[i] + random.randrange(-30,30))

        sql = "INSERT INTO data_tb (datetime, val) VALUES (%s, %s)"
        val = (current, data[i])

        mycursor.execute(sql, val)

        current = current + datetime.timedelta(hours=1)
    
    cnt = cnt + 1
    
    
print(mycursor.rowcount, "record inserted")
conn.commit()


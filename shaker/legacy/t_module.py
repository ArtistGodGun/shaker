from itertools import *
import time

def setRhythmCase(): # 8분음표 단위의 쉼표를 제외한 모든 리듬
    basic_source = [2,4,6,8,10,12,14]
    # basic_source = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    total_pattern = [[16], [2,2,2,2,2,2,2,2,]]
    # total_pattern = []

    a = 1
    start = time.time()
    while a < len(basic_source):
        for i in product(basic_source, repeat = a):
            if sum(list(i)) == 16 and list(i) not in total_pattern:
                # print(i)
                total_pattern.append(list(i))
        a+=1

    arp = {}
    for index, i in enumerate(total_pattern):
        arp[f'pattern{index+1}'] = i
    return arp

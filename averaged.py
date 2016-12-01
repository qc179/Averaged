#!/usr/bin/python3
# -*- coding: utf-8 -*-
# filename:averaged.py

import xlrd
import sys
import time
from collections import deque

id_val_xls = xlrd.open_workbook('weibo_bids.xls')
id_val_sheet1 = id_val_xls.sheets()[0]
id_val_list = []
for row in range(id_val_sheet1.nrows):
    # 把id化整后字符串化
    id = str(int(id_val_sheet1.cell(row, 0).value))
    # 把文章数化整
    artnum = int(id_val_sheet1.cell(row, 1).value)
    # 添加到列表
    id_val_list.append((id, artnum))

# 转换成字典
id_val_dict = dict(id_val_list)
val_list = list(id_val_dict.values())
val_list_len = len(val_list)
val_list_sum = sum(val_list)
val_list.sort(reverse=True)
val_list_queue = deque(val_list)
print('读取到以下这些值：')
print(val_list)
print('*' * 79)

print('共有', len(id_val_dict), '个值需要分组，总和等于', val_list_sum)
spider_num = int(input('需要均分为几组，请输入：'))
avg_target = int(val_list_sum / spider_num)
print('将以每组值合计约等于', avg_target, '为目标对所有值进行分组')
time.sleep(1)
print('开始分组...\n')
time.sleep(1)

ready_group = []
ready_group_num = 0
group_list = []
while len(val_list_queue) > 0:
    ready_group_num_0 = len(ready_group)
    if ready_group_num_0 == 0:
        ready_group_sum = 0
    else:
        ready_group_sum = sum(ready_group)

    # 判断readygroup是否达成目标，达成则break
    if ready_group_num == val_list_len:
        print(ready_group)
        group_list.append(ready_group)
        print('---单组合计', ready_group_sum, '相差均值', ready_group_sum - avg_target)
        print('共', ready_group_num, '个数值，全部完成均分')
        break
    elif abs(avg_target - ready_group_sum) < min(val_list_queue):
        print(ready_group)
        group_list.append(ready_group)
        print('--单组合计', ready_group_sum, '相差均值', ready_group_sum - avg_target)
        ready_group = []
    elif ready_group_sum >= avg_target:
        print(ready_group)
        group_list.append(ready_group)
        print('-单组合计', ready_group_sum, '相差均值', ready_group_sum - avg_target)
        ready_group = []

    if len(val_list_queue) == 1:
        cur = val_list_queue.popleft()
        ready_group.append(cur)
        ready_group_num += 1
        print(ready_group)
        group_list.append(ready_group)
        print('---单组合计', sum(ready_group), '相差均值', sum(ready_group) - avg_target)
        print('\n共', ready_group_num, '个数值，全部完成均分')
        break
    else:
        cur = val_list_queue.popleft()
        if cur >= avg_target:
            ready_group.append(cur)
            ready_group_num += 1
            print(ready_group)
            group_list.append(ready_group)
            print('大于均值 相差均值', sum(ready_group) - avg_target)
            ready_group = []
            continue
        else:
            curx = abs(avg_target - ready_group_sum - cur)
            oxlist = [abs(avg_target - ready_group_sum - o) for o in val_list_queue]
            ox = min(oxlist)
            if curx <= ox:
                ready_group.append(cur)
                ready_group_num += 1
            else:
                val_list_queue.append(cur)

print('\n----以下为对应id的分组----')
id_val_list = deque(id_val_list)

wresult = open('result.txt', 'w')

for gl in group_list:
    id_group = []
    for gi in gl:
        while True:
            idque = id_val_list.popleft()
            if gi != idque[1]:
                id_val_list.append(idque)
            else:
                id_group.append(int(idque[0]))
                break
    print(id_group)
    wresult.write(str(id_group))
    wresult.write('\n')

wresult.close()

print('*' * 78)
anyenter = input("Grouped completed.Press Enter to quit.")
sys.exit()

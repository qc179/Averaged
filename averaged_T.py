#!/usr/bin/python3
# -*- coding: utf-8 -*-

import xlrd
import sys
import time
from collections import deque


def usetm(input_val):
    if input_val < 1500:
        tm = round((input_val / 20), 2)
    else:
        tm = round((input_val / 25), 2)
    return tm


id_val_xls = xlrd.open_workbook('weibo_bids.xls')
id_val_sheet1 = id_val_xls.sheets()[0]
id_val_list = []
val_list = []
id_tm_list = []
tm_list = []

# 读取文件，同时计算各val的tm
for row in range(id_val_sheet1.nrows):
    row0 = str(int(id_val_sheet1.cell(row, 0).value))
    row1 = int(id_val_sheet1.cell(row, 1).value)
    val_use_tm = usetm(row1)
    id_val_list.append((row0, row1))
    val_list.append(row1)
    id_tm_list.append((row0, val_use_tm))
    tm_list.append(val_use_tm)

# val_list
val_list_len = len(val_list)
val_list_sum = sum(val_list)
val_list.sort(reverse=True)

# tm_list
tm_list_len = len(tm_list)
tm_list_sum = sum(tm_list)
tm_list.sort(reverse=True)

print('共 %s 个值，值合计 %s' % (val_list_len, val_list_sum))
month_num = int(input('初始化时长几个月（不足一月输入0），请输入：'))

month_num += 1
base_tm = round(val_list_len * month_num * 1.5, 2)
all_tm = base_tm + tm_list_sum

groups_num = int(input('把这些值均分为几组，请输入：'))
avg_tm = round(all_tm / groups_num, 2)
print('...\n分组计划：\n%s 个值，分成 %s 组\n每组用时约合 %sm(%sh)'
      %
      (val_list_len,
       groups_num,
       avg_tm,
       round(avg_tm / 60, 1)))

time.sleep(1)
print('...')
time.sleep(1)
print('...')
time.sleep(1)

# 将tm分组
tm_list_que = deque(tm_list)
tm_groups = [[] for a in range(groups_num)]
tm_groups_idx = [x for x in range(groups_num)]

while len(tm_list_que) > 0:
    for i in tm_groups_idx:
        if len(tm_list_que) == 0:
            break
        group_tm = sum(tm_groups[i]) + int(len(tm_groups[i]) * month_num * 1.5)
        if group_tm >= avg_tm:
            continue
        tm_groups[i].append(tm_list_que.popleft())
    tm_groups_idx.reverse()

# 依照tm分组遍历id_tm_list组成对应id分组，同时保存结果到文件
id_tm_list_que = deque(id_tm_list)
id_groups = []

with open('result.txt', 'w') as savetxt:
    savetxt.write('分组的 id ：\n')
    for tm_group in tm_groups:
        id_group = []
        for tm in tm_group:
            while True:
                id_tm_left = id_tm_list_que.popleft()
                if tm != id_tm_left[1]:
                    id_tm_list_que.append(id_tm_left)
                else:
                    id_group.append(int(id_tm_left[0]))
                    break
        id_groups.append(id_group)
        id_group = str(id_group)
        id_group = id_group.replace('[', '##')
        id_group = id_group.replace(']', '')
        id_group = id_group.replace(' ', '')
        savetxt.write(id_group)
        savetxt.write('\n')

# 依照id分组遍历id_val_list组成对应val分组
id_val_list_que = deque(id_val_list)
val_groups = []

for id_group in id_groups:
    val_group = []
    for Id in id_group:
        while True:
            id_val_list_left = id_val_list_que.popleft()
            if Id != int(id_val_list_left[0]):
                id_val_list_que.append(id_val_list_left)
            else:
                val_group.append(int(id_val_list_left[1]))
                break
    val_groups.append(val_group)

print('>>>值(value)的分布情况')
for i in range(groups_num):
    print('%s Group %s %s' % ('-' * 34, i + 1, '-' * 35))
    print(val_groups[i])

print('\n>>>用时(time)分布情况')
ii = 1
for tm_group in tm_groups:
    print(ii, tm_group)
    ii += 1

print('\n>>>统计')
groups_cnt = 0
groups_sum = 0
for i in range(groups_num):
    val_groups_tm = 0
    for vg in val_groups[i]:
        val_groups_tm += usetm(vg)
    val_groups_tm += int(len(val_groups[i]) * month_num * 1.5)
    print('Group %s:Count %s Value %s Time %sm(%sh)' %
          (i + 1,
           len(tm_groups[i]),
           sum(val_groups[i]),
           val_groups_tm,
           round(val_groups_tm / 60, 1)))
    groups_cnt += len(val_groups[i])
    groups_sum += sum(val_groups[i])

print('\n>>>结束')
print(groups_cnt, '个值参与分组，结果已经保存到 result.txt\n')

anyenter = input("\n按回车键退出.")
sys.exit()

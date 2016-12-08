#!/usr/bin/python3
# -*- coding: utf-8 -*-

import xlrd
import sys
import time
from collections import deque


def usetm(input_val):
    if input_val < 1500:
        tm = int(input_val / 20)
    else:
        tm = int(input_val / 25)
    return tm

id_val_list = []
id_tm_list = []
id_val_xls = xlrd.open_workbook('weibo_bids.xls')
id_val_sheet1 = id_val_xls.sheets()[0]

for row in range(id_val_sheet1.nrows):
    row0 = str(int(id_val_sheet1.cell(row, 0).value))
    row1 = int(id_val_sheet1.cell(row, 1).value)
    id_val_list.append((row0, row1))

# 先把值取出来单独组成列表
val_list = list(dict(id_val_list).values())
val_list_len = len(val_list)
val_list_sum = sum(val_list)
val_list.sort(reverse=True)
tm_list = []

for id_val in id_val_list:
    val_use_tm = usetm(id_val[1])
    id_tm_list.append((str(id_val[1]), int(val_use_tm)))

for val in val_list:
    val_tm=usetm(val)
    tm_list.append(val_tm)

print(tm_list)
tm_list_len = len(tm_list)
tm_list_sum = sum(tm_list)
tm_list.sort(reverse=True)

month_num = 12
basetime = val_list_len *month_num*1.5

print('basetime=%s tmsum=%s alltm=%s' % (basetime,tm_list_sum,basetime+tm_list_sum))
print('共有', val_list_len, '个值，合计', val_list_sum)
spider_num = int(input('把这些值均分为几组，请输入：'))
avg_target = int(val_list_sum / spider_num)
avg_tm = int((basetime+tm_list_sum) / spider_num)
print('分组计划：', val_list_len,
      '个值，分成', spider_num,
      '组，每组约合', avg_target, '(', val_list_sum, '/', spider_num, ')',
      '每组理想时间',avg_tm)

time.sleep(1)
print('...')
time.sleep(1)
print('...')
time.sleep(1)

id_group_val0 = []
for id_val in id_val_list:
    if id_val[1] == 0:
        id_group_val0.append(int(id_val[0]))
    else:
        pass
id_group_val0_len = len(id_group_val0)

# 去除0
cnt0 = val_list.count(0)
for i in range(cnt0):
    val_list.remove(0)

# 创建最外层列表，用于存放所有分组
groups = []
for o in range(spider_num):
    groups.append([])

# 创建队列
val_list_queue = deque(val_list)

# 创建一个列表作为各个分组的索引
groups_idx = [i for i in range(spider_num)]

# 分组步骤：
# 1、把各值由大到小分依次配到各组
# 2、各组都得到一个新值后，逆序索引，重复第一步，直到队列为空
# 3、当一组满足目标时就跳出，不再参与分配
while len(val_list_queue) > 0:
    for i in groups_idx:
        if len(val_list_queue) == 0:
            break
        if sum(groups[i]) >= avg_target:
            continue
        groups[i].append(val_list_queue.popleft())
    # 把索引逆序就可以在下一轮for中反向对各组循环
    groups_idx.reverse()

tm_groups = []
for s in range(spider_num):
    tm_groups.append([])

tm_list_que = deque(tm_list)

groups_idx = [i for i in range(spider_num)]

print(tm_list_que)
while len(tm_list_que) > 0:
    for i in groups_idx:
        if len(tm_list_que) == 0:
            break
        group_tm = sum(tm_groups[i]) + int(len(tm_groups[i])*month_num*1.5)
        print(tm_groups[i])
        print(group_tm)
        if group_tm >= avg_tm:
            continue
        tm_groups[i].append(tm_list_que.popleft())
    groups_idx.reverse()

print('>>>>>>')
for tm_group in tm_groups:
    group_tm = sum(tm_group) + int(len(tm_group) * month_num * 1.5)
    print(tm_group)
    print(group_tm)
print(tm_list_que)

id_val_list_queue = deque(id_val_list)

# with open('result.txt', 'w') as savetxt:
#     savetxt.write('分组的 id ：\n')
#     for group in groups:
#         id_group = []
#         for val in group:
#             while True:
#                 id_left = id_val_list_queue.popleft()
#                 if val != id_left[1]:
#                     id_val_list_queue.append(id_left)
#                 else:
#                     id_group.append(int(id_left[0]))
#                     break
#         id_group = str(id_group)
#         id_group = id_group.replace('[', '##')
#         id_group = id_group.replace(']', '')
#         id_group = id_group.replace(' ', '')
#         savetxt.write(id_group)
#         savetxt.write('\n')
#     savetxt.write('\n未参与分组的 id ：\n')
#     id_group_val0 = str(id_group_val0)
#     id_group_val0 = id_group_val0.replace('[', '##')
#     id_group_val0 = id_group_val0.replace(']', '')
#     id_group_val0 = id_group_val0.replace(' ', '')
#     savetxt.write(id_group_val0)

print('>>>值的分布情况')
for i in range(spider_num):
    print('-' * 34 + ' Group', i + 1, '-' * 35)
    print(groups[i])

print('>>>统计')
groups_cnt = 0
groups_sum = 0
for i in range(spider_num):
    print('Group', i + 1, 'count', len(groups[i]), 'sum', sum(groups[i]))
    groups_cnt += len(groups[i])
    groups_sum += sum(groups[i])

print('>>>完成')
print(id_group_val0_len, '个值等于零，未参与分组')
print(groups_cnt, '个值参与分组，合计', groups_sum)
print('分组结果已经保存到 result.txt\n')




i = 0
all_val_use_tm = 0
for group in groups:
    i += 1
    print('group', i)
    group_use_tm = 0
    for val in group:
        val_use_tm = usetm(val)
        # print('val=%s need_time=%s' % (val,val_use_tm))
        group_use_tm += val_use_tm
    base_tm = int(len(group) * 12 * 1.5)
    group_use_tm += base_tm
    all_val_use_tm += group_use_tm
    print('count=%s group_need_time=%s' % (len(group), group_use_tm))
print('all_val_ues_tm=',all_val_use_tm)

anyenter = input("\n按回车键退出.")
sys.exit()

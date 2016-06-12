#!/usr/bin/env python
#-*- coding: utf-8 -*-
#filename:averaged.py
#Auto grouped weibo's bid averaged before init
#This tool works with weibo_bids.xls in current work file
#weibo_bids.xls:col0 is id,col1 is number

import xlrd
from collections import deque

getbids = xlrd.open_workbook('weibo_bids.xls')
bids_sheet1 = getbids.sheets()[0]
bids_list = []
for row in range(bids_sheet1.nrows):
    #把bid化整后字符串化
    bid = str(int(bids_sheet1.cell(row,0).value))
    #把文章数化整
    artnum = int(bids_sheet1.cell(row,1).value)
    #添加到列表
    bids_list.append((bid,artnum))
#转换成字典
bids_dict = dict(bids_list)
print u'共有',len(bids_dict),u'个id需要分组'

val_list = bids_dict.values()
val_list_len = len(val_list)

val_sum = sum(val_list)
print u'\n全部id总计和为',val_sum

val_list.sort(reverse=True)
val_queue = deque(val_list)

print u'\n需要均分为几组：'
spider_num = raw_input()
spider_num = int(spider_num)

avg_target = val_sum/spider_num
print u'\n目标均值：',avg_target,'\n'

group = []
group_num = 0
group_list = []
while len(val_queue)>0:
    group_len = len(group)
    if group_len == 0:
        group_sum = 0
    else:
        group_sum = sum(group)

    if group_num == val_list_len:
        print group
        group_list.append(group)
        print u'---单组合计',group_sum,u'相差均值',group_sum-avg_target
        print u'共',group_num,u'个数值，全部完成均分'
        break
    elif abs(avg_target-group_sum) < min(val_queue):
        print group
        group_list.append(group)
        print u'--单组合计',group_sum,u'相差均值',group_sum-avg_target
        group = []
    elif group_sum >= avg_target:
        print group
        group_list.append(group)
        print u'-单组合计',group_sum,u'相差均值',group_sum-avg_target
        group = []


    if len(val_queue) == 1:
        cur = val_queue.popleft()
        group.append(cur)
        group_num += 1
        print group
        group_list.append(group)
        print u'---单组合计',sum(group),u'相差均值',sum(group)-avg_target
        print u'\n共',group_num,u'个数值，全部完成均分'
        break
    else:
        cur = val_queue.popleft()
        if cur >= avg_target:
            group.append(cur)
            group_num += 1
            print group
            group_list.append(group)
            print u'大于均值 相差均值',sum(group)-avg_target
            group = []
            continue
        else:
            curx = abs(avg_target-group_sum-cur)
            oxlist = [abs(avg_target-group_sum-o) for o in val_queue]
            ox = min(oxlist)
            if curx <= ox:
                group.append(cur)
                group_num += 1
            else:
                val_queue.append(cur)

print u'\n----以下为对应id的分组----\n'
bids_list = deque(bids_list)

for gl in group_list:
    bid_group = []
    for gi in gl:
        while True:
            bidque = bids_list.popleft()
            if gi != bidque[1]:
                bids_list.append(bidque)
            else:
                bid_group.append(int(bidque[0]))
                break
    print bid_group

print '*'*75
anyenter = raw_input('Grouped completed.Press Enter to quit.')
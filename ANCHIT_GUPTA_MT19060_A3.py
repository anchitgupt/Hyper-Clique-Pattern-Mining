#!/usr/bin/env python
# coding: utf-8
#
# Name: Anchit Gupta
# Roll no: MT19060
# DMG A3




### Before Running please update the min_supp (line 219) and cross support graph indices (line 335)

import pandas as pd
import numpy as np
import time 
from tqdm import tqdm_notebook as tqdm
import matplotlib.pyplot as plt
tqdm().pandas()



filename='pumsb.dat'
df = pd.read_csv(filename, header=None)
df.head()
shape = df.shape


def unique(list1): 
    x = np.array(list1) 
    l = np.unique(x)
    return l

items_name = frozenset()
row_data = []

with open(filename) as f:
    lines = f.readlines()
    for l in tqdm(lines, miniters=10000):
        k = l.split()
        if (k[len(k)-1] == '\n'):
            k = k[:len(k)-1]
        k = list(map(int, k))
        row_data.append(k)
        t = unique(k)
        np.sort(t)
        items_name= items_name | frozenset(t)
#         items_name.append(t)
items_name = list(items_name)
items_name = unique(items_name)
print(items_name)
print(len(items_name))



print (len(row_data[0]))



d = pd.DataFrame(0, index=np.arange(shape[0]), columns=items_name)
d.values


k = d.values
np_items_name = items_name[:]
np.array(np_items_name)

np_row_data = row_data[:]
np.array(np_row_data)

t1 = time.time()
c = 0
for i in tqdm(np_row_data):
    d.loc[c] = np.isin(np_items_name, i).astype(int)
    c+=1    

print(time.time()-t1)
d.head()


frequency_items = dict(d.sum())
total_sum = d.sum().sum()


total_transaction = len(row_data)
total_transaction




support_items_indv = {}
for k in frequency_items:
    support_items_indv[k] = float(frequency_items[k]/total_transaction)



def getMinListAccSupport(isupp):
    temp_l = []
    k = sorted(support_items_indv.items(), key=lambda kv: kv[1], reverse=True)
    for i in k:
        if i[1] >= isupp:
            temp_l.append(i[0])
    return temp_l



def getCrossSupportIndexIndv(ilist, hconfi):
    b = []
    fi = []
    i=0
    for i in range(len(ilist)-1):
        b = []
        for j in range(i+1,len(ilist)):
            f = ilist[j]
            l = ilist[i]
            cond = support_items_indv[f] < (hconfi * support_items_indv[l])
            if cond == False:
                if ilist[i] not in b:
                    b.append(ilist[i])
                b.append(ilist[j])
            else:
                break
        if b not in fi and len(b) != 0:
            fi.append(b)
    return fi



def getCrossSupportIndex(ilist, hconfi):
    b = []
    fi = []
    i=0
    for i in range(len(ilist)-1):
        b = []
        for j in range(i+1,len(ilist)):
            cond =  (hconfi * supp_dict[ilist[i]]) > supp_dict[ilist[j]] 
            if cond == False:
                if ilist[i] not in b:
                    b.append(ilist[i])
                b.append(ilist[j])
            else:
                break
        if b not in fi and len(b) != 0:
            fi.append(b)
    return fi



def mergable(s1, s2, size):
    if(type(s1) == int and type(s2) ==  int):
        return True
    else:
        l1 = sorted(list(s1))
        l2 = sorted(list(s2))
        if l1[:-1] == l2[:-1]:
            return True
        else:
            return False



def merge(s1, s2): 
    if(type(s1) == int and type(s2) ==  int):
        s = frozenset([s1, s2])
        return s
    s3 =  s1 | s2
    return frozenset(s3)


def getHConf(l, temp_sup):
    deno = 0
    l = list(l)
    for i in l:
        if deno < support_items_indv[i]:
            deno = support_items_indv[i]
    return temp_sup/deno



def getSupport(l, size):
    l = list(l)
    df = d[l]
    df = df.sum(axis=1).to_frame()
    sup = (df[0] == size).sum() / total_transaction
    return sup


def getElements(crossDList, ihconf, isupp, size):
    cDict = []
    temp_dict = {}
    for itemsList in crossDList:
        for i in range(len(itemsList)):
            for j in range(i+1, len(itemsList)):
                if mergable(itemsList[i], itemsList[j], size):
                    k = merge(itemsList[i], itemsList[j])
                    s = getSupport(k, size)
                    if s >= isupp:
                        h = getHConf(k, s)
                        if h >= ihconf:
                            supp_dict[k] = s
                            temp_dict[k] = s
                            cDict.append(k)
    return cDict, temp_dict




def getSortedAccSupport(temp_ilist, temp_dict):
    temp_list = []
    for key, value in sorted(temp_dict.items(), key=lambda item: item[1],reverse=True):
        temp_list.append(key)
    return temp_list




pt = {}
tm = {}
min_hconf = [ 0.93 , 0.95]
min_supp  = [.5]
supp_dict = {}
for ihconf in min_hconf:
    print('\nHconf ', ihconf)
    temp_ilist = []
    s_list = []
    t_list = [] #storing time
    for isupp in min_supp:
        t1 = time.time()
        s_size = 0
        print("Support ", isupp)
        ilist = getMinListAccSupport(isupp)
        s_size = len(ilist)
        print("Size:  1", "Patterns:", len(ilist))
        for size in range(2, 12):
            if (size == 2):
                crossDList = getCrossSupportIndexIndv(ilist, ihconf)
            else:
                if len(temp_ilist) == 0:
                    break
                ilist = temp_ilist[:]
                temp_ilist = []
                crossDlist = [] 
                crossDList = getCrossSupportIndex(ilist, ihconf)
            temp_ilist, temp_dict = getElements(crossDList, ihconf, isupp, size)
            temp_ilist = getSortedAccSupport(temp_ilist, temp_dict)
            s_size+=len(temp_ilist)
            print("Size: ", size, "Patterns:", len(temp_ilist))
        s_list.append(s_size)    
        print("Overall Size: ", s_size)
        t_list.append(time.time() - t1)
        
    pt[ihconf] = s_list
    tm[ihconf] = t_list

print(pt)
print(tm)



min_supp1  = [.4, .45, .5]
plt.figure(figsize=(8, 8))
plt.plot(min_supp1, pt[min_hconf[0]])
plt.plot(min_supp1, pt[min_hconf[1]])
plt.legend(["Hconf: .93", "Hconf: .95"])
plt.title("Confidence Pruning Effect")
plt.xlabel('Minimum Support Threshold')
plt.ylabel('Number of HyperClique Pattern')

plt.figure(figsize=(8,8))
plt.plot(min_supp1, tm[min_hconf[0]])
plt.plot(min_supp1, tm[min_hconf[1]])
plt.legend(["Hconf: .93", "Hconf: .95"])
plt.title("Hconf")
plt.xlabel('Minimum Support Threshold')
plt.ylabel('Execution Time (sec)')


def getCrossSupportIndex2(ilist, hconfi):
    b = []
    fi = []
    i=0
    for i in range(len(ilist)-1):
        b = []
        for j in range(i+1,len(ilist)):
            if ilist[i] not in b:
                    b.append(ilist[i])
            b.append(ilist[j])
        fi.append(b)
    return fi


pt1 = {}
tm1 = {}
min_supp  = [.5]
supp_dict = {}
for ihconf in min_hconf:
    print('\nHconf ', ihconf)
    temp_ilist = []
    s_list = []
    t_list = [] #storing time
    for isupp in min_supp:
        t1 = time.time()
        s_size = 0
        print("Support ", isupp)
        ilist = getMinListAccSupport(isupp)
        s_size = len(ilist)
        print("Size:  1", "Patterns:", len(ilist))
        for size in range(2, 12):
            if (size == 2):
                crossDList = getCrossSupportIndex2(ilist, ihconf)
            else:
                if len(temp_ilist) == 0:
                    break
                ilist = temp_ilist[:]
                temp_ilist = []
                crossDlist = [] 
                crossDList =  getCrossSupportIndex2(ilist, ihconf)
            temp_ilist, temp_dict = getElements(crossDList, ihconf, isupp, size)
            temp_ilist = getSortedAccSupport(temp_ilist, temp_dict)
            s_size+=len(temp_ilist)
            print("Size: ", size, "Patterns:", len(temp_ilist))
        s_list.append(s_size)    
        print("Overall Size: ", s_size)
        t_list.append(time.time() - t1)
        
    pt1[ihconf] = s_list
    tm1[ihconf] = t_list

print(pt1)
print(tm1)



plt.figure(figsize=(8, 8))
plt.plot(min_hconf[::-1], [tm1[min_hconf[1]],tm1[min_hconf[0]]])
plt.plot(min_hconf[::-1], [tm[min_hconf[1]][0],tm[min_hconf[0]][0]])
plt.legend(["Anti Monotone", "Anti Monotone + Cross Support"])
plt.title("Cross Support Importance")
plt.xlabel('Hconfidence')
plt.ylabel('Execution time')


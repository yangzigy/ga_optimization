#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import json
import os
import sys
import time
from ctypes import *  
import random
import math
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
import ga

img_x=range(-20,20)
img_y=range(-20,20)
img_z=[]

max_z=[]
for x in img_x:
	x=x/10
	tr=[]
	for y in img_y:
		y=y/10
		tr.append(-x*y/math.exp(x*x+y*y))
	img_z.append(tr)
	max_z.append(max(tr))
print(max(max_z))

def para_2_x(para): #解码
	return para/65536.0*4-2 #首先将0~1范围解算成值域
total_eval=0 #总运行次数
def eval_fun(para): #测试评价函数
	global total_eval
	total_eval+=1
	x=para_2_x(para[0])
	y=para_2_x(para[1])
	z=-x*y/math.exp(x*x+y*y) #评价函数本身
	return z

population=[]
for x in range(16):
	t=ga.DNAbase()
	population.append(t)
ga=ga.GA(population,2,eval_fun)
ga.ini()
for x in range(10):
	ga.run()
	print(x,end='	') #代数
	for y in ga.population:
		print('%.3f'%y.score,end=',[')
		for z in y.para:
			print('%.2f'%para_2_x(z),end=',')
		print('],',end='')
	print()
print('total: '+str(total_eval))

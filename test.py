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
import ga

img_x=range(200)
img_y=[x/20.0*math.sin(3*x/20.0) for x in img_x]
#fig=plt.figure(figsize=(100,100))
#fig.patch.set_color("g")
fig=plt.figure()
plt.subplot(111,axisbg=(0.5,0.5,0.5))
plt.plot([x/20.0 for x in img_x],img_y,label="$xsin(3x)$",color=(1,0,0),linewidth=1)
#plt.legend()
#print(img_y)

def para_2_x(para): #解码
	return para/65536.0*10 #首先将0~1范围解算成值域
total_eval=0 #总运行次数
def eval_fun(para): #测试评价函数
	global total_eval
	total_eval+=1
	x=para_2_x(para[0])
	y=x*math.sin(3*x) #评价函数本身
	return y

population=[]
for x in range(15):
	t=ga.DNAbase()
	population.append(t)
ga=ga.GA(population,1,eval_fun)
ga.ini()
plt.scatter([para_2_x(x.para[0]) for x in ga.population],[x.score for x in ga.population],c=(1,1,0),s=50,marker='*')
for x in range(7):
	#fig=plt.figure()
	#plt.subplot(111,axisbg=(0.5,0.5,0.5))
	#plt.plot([x/10.0 for x in img_x],img_y,label="$xsin(3x)$",color=(1,0,0),linewidth=1)
	#plt.scatter([para_2_x(x.para[0]) for x in ga.population],[x.score for x in ga.population],c=(1,1,0),s=50,marker='*')
	ga.run()
	print(x,end='	') #代数
	for y in ga.population:
		print('%.3f'%y.score,end=',[')
		for z in y.para:
			print('%.2f'%para_2_x(z),end=',')
		print('],',end='')
	print()
	#tmp=0
	#for x in ga.population:
		#tmp+=1
		#xx=[para_2_x(y[0][0]) for y in x.test_rec]
		#yy=[y[1] for y in x.test_rec]
		#print(xx,yy)
		#print(len(xx))
		#color=((tmp & 0x04)>>2,(tmp & 2)>>1,tmp & 1)
		#print(tmp,color)
		#plt.plot(xx,yy,label="$jump$",color=color,linewidth=1)
	#plt.scatter([para_2_x(x.para[0]) for x in ga.population],[x.score for x in ga.population],c=(1,0,1),s=50,marker='o')
	#plt.show()

plt.scatter([para_2_x(x.para[0]) for x in ga.population],[x.score for x in ga.population],c=(1,0,1),s=50,marker='o')
#画所有的跳动线
#tmp=0
#for x in ga.test_pop: #对于生过的每一个个体
	#tmp+=1
	#xx=[para_2_x(y[0][0]) for y in x.test_rec]
	#yy=[y[1] for y in x.test_rec]
	##print(xx,yy)
	##print(len(xx))
	#color=((tmp & 0x04)>>2,(tmp & 2)>>1,tmp & 1)
	##print(tmp,color)
	#plt.plot(xx,yy,label="$jump$",color=color,linewidth=1)

#画最好的跳动线
xx=[para_2_x(y[0][0]) for y in ga.population[0].test_rec]
yy=[y[1] for y in ga.population[0].test_rec]
print(len(xx),total_eval)
plt.plot(xx,yy,label="$jump$",color='b',linewidth=1)

#绘图
plt.show()

#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import json
import os
import sys
import time
from ctypes import *  
import random

class DNAbase: #需要用户初始化参数序列个数
	def __init__(self):
		self.score=0 #得分
		self.para=[] #参数序列,是一个16位整形定点数，无符号，数量必须是偶数
		self.test_rec=[] #记录参数和分数
	def __str__(self):
		return '%f,%s'%(self.score,[x for x in self.para])
	def __lt__(self,other):
		return self.score<other.score
	def ini(self,para_n): #初始化一个dna
		self.para=(c_ushort*para_n)()
		for x in range(len(self.para)):
			self.para[x]=c_ushort(random.randint(0,65536))
	def cross(self,dna,cross_pos): #交叉算法,输入交叉位置(低位起),和另一个dna
		outdna1=type(self)()
		outdna1.para=(c_ushort*len(self.para))()
		outdna2=type(self)()
		outdna2.para=(c_ushort*len(self.para))()
		mask_h=0xffffffff << cross_pos #高位掩码
		mask_l=(1 << cross_pos)-1 #低位掩码
		c=0
		for x in zip(self.para,dna.para):
			t=(x[0] & mask_h) | (x[1] & mask_l)
			outdna1.para[c]=c_ushort(t)
			t=(x[1] & mask_h) | (x[0] & mask_l)
			outdna2.para[c]=c_ushort(t)
			c+=1
		return (outdna1,outdna2)
	def mutation(self,rate): #基因突变,输入变异率
		for x in range(len(self.para)):
			r=random.random()
			if r<rate: #若需要突变
				#求突变位置
				r=int(r/rate*16)
				self.para[x] ^= (1<<r)
class GA:
	def __init__(self,population,para_n,eval_fun):  #要求客户初始化种群，数量必须是偶数，输入参数个数
		self.cross_pos=13 #交叉位数
		self.cross_pos_delta=0 #交叉位数变化
		self.mutation_rate=0.5

		self.population=population
		self.para_n=para_n
		self.eval_fun=eval_fun
		
		self.test_pop=[]
		self.test_pop.extend(population) #测试种群
	def ini(self): #初始化
		for x in self.population: #全部初始化
			x.ini(self.para_n)
		#评价第一批个体
		for x in self.population:
			x.score=self.eval_fun(x.para)
			x.test_rec.append((x.para,x.score))
	def select_dna(self,acc): #选取dna，输入所有得分累加
		r=random.random()*acc
		for x in self.population:
			r-=x.score
			if r<=0:
				return x
		return self.population[0]
	def learn(self,pop,step): #输入要学习的个体,学习步长
		for x in pop:
			t=(c_ushort*len(x.para))()
			for y in range(len(t)): #给新的参数赋值
				t[y]=x.para[y]+random.randint(-step,step)
				if t[y]>65536:
					print(type(t[0]),type(x.para[0]),t)
			score=self.eval_fun(t) #评价
			if score>x.score: #若学的比较好，就接受
				x.para=t
				x.score=score
				x.test_rec.append((x.para,x.score))

	def run(self): #执行一代
		#选取个体交配
		population_new=[]
		acc=0 #所有得分累加
		for x in self.population:
			acc+=x.score
		for x in range(int(len(self.population)/4)):
			dna1=self.select_dna(acc)
			dna2=self.select_dna(acc) #选择
			dna3,dna4=dna1.cross(dna2,self.cross_pos+ #交叉
				random.randint(-self.cross_pos_delta,self.cross_pos_delta))
			dna3.mutation(self.mutation_rate)
			dna4.mutation(self.mutation_rate) #变异
			dna3.score=self.eval_fun(dna3.para)
			dna4.score=self.eval_fun(dna4.para) #评价
			population_new.append(dna3)
			population_new.append(dna4) #加入新生缓存
			self.test_pop.append(dna3)
			self.test_pop.append(dna4)
			dna3.test_rec.extend(dna1.test_rec)
			dna4.test_rec.extend(dna2.test_rec)
			dna3.test_rec.append((dna3.para,dna3.score))
			dna4.test_rec.append((dna4.para,dna4.score))
		#全体学习
		self.learn(self.population,3000)
		self.learn(population_new,3000)
		self.population.sort(reverse=True) #排序
		for x in range(len(population_new)):#覆盖排名后50%
			self.population[len(self.population)-x-1]=population_new[x]


# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 08:54:35 2021

@author: CongWei
"""
import matplotlib.pyplot as plt 
import numpy as np


GEAR_RATIO = 6.32         #传动比
WHEEL_DIAMETER = 805      #半磨耗轮径 mm
SELF_WEIGHT = 56          #自重 t
LOAD_WEIGHT = 56          #负载重量 t
GRADE = 0                 #坡道坡度 千分之一
G = 9.81                  #重力加速度
AXLE_NUM = 4              #车轴数
MOTOR_EFF = 0.95          #电机效率
GEAR_EFF = 0.985          #传动箱效率
MAX_V_REMAIN_ACC = 0.065  #最高速度要求剩余加速度
MIN_V = 16.9              #恒功运行最低速度 km/h
MAX_V = 88                #恒功运行最高速度 km/h

RESISTANT_MAX_V =  6.2134 #最高速度时总阻力 kN



                             
                             
                             
                           
class TractionSystem:
    def __init__(self,start,end,plot_num):
        self.array_v = np.linspace(start,end,plot_num)              #速度数组 km/h
        self.max_v_traction_effort = 0                              #恒功运行最高速度要求牵引力 kN
        self.power_constant = 0                                     #恒功功率 kW
        self.array_traction_effort = []                             #牵引力数组 kN
    
    
    def calculation_power_constant(self):
        self.max_v_traction_effort = MAX_V_REMAIN_ACC * (SELF_WEIGHT + LOAD_WEIGHT) + RESISTANT_MAX_V
        self.power_constant = self.max_v_traction_effort * MAX_V/3.6
    
    
    def calculation_single_traction_effort(self,power,velocity):
        if velocity <=MIN_V:
            traction_effort = power*3.6/MIN_V
        elif velocity < MAX_V:
            traction_effort = power*3.6/velocity
        else:
            traction_effort = self.max_v_traction_effort*MAX_V*MAX_V/(velocity*velocity)
        return traction_effort
        
        
    def calculation_array_traction_effort(self):
        self.calculation_power_constant()
        for v in self.array_v:
            effort = self.calculation_single_traction_effort(self.power_constant, v)
            self.array_traction_effort.append(effort)
           
         
            
    def plot_v_traction_efforts(self):
        self.calculation_array_traction_effort()
        
        plt.style.use('seaborn')
        fig,ax = plt.subplots()

        ax.scatter(self.array_v,self.array_traction_effort,color=(0,0.8,0),s=10) # color=RGB 红绿蓝

        ax.set_title("V-F",fontsize = 24)
        ax.set_xlabel("v",fontsize = 14)
        ax.set_ylabel("traction_effort",fontsize = 14)
        ax.tick_params(axis='both',labelsize=14)

        #plt.show()
        plt.savefig('V-F-curver.png',bbox_inches='tight')
            

myloco = TractionSystem(0,100,1000)

myloco.plot_v_traction_efforts()
    
   
    

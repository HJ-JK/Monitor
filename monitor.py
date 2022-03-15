#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 10:26:38 2022

@author: hanjiezhu
"""

from multiprocessing import Process
from multiprocessing import Condition, Lock
from multiprocessing import Value
from multiprocessing import current_process
import time, random

class Table():
    def __init__(self, size: int, manager):
        self.phil = None
        self.size = size
        self.fork = manager.list([False]*self.size)
        self.mutex = Lock()
        self.can_eat = Condition(self.mutex)

    def have_fork(self):
        return not(self.fork[(self.phil-1)%self.size] or self.fork[(self.phil+1)%self.size])
    
    def set_current_phil(self,num):
        self.phil = num  
    
    def wants_eat(self, num):
        self.mutex.acquire()
        self.can_eat.wait_for(self.have_fork)
        self.fork[num] = True
        self.mutex.release()

    def wants_think(self, num):
        self.mutex.acquire()
        self.fork[num] = False
        self.can_eat.notify_all()
        self.mutex.release()


class CheatMonitor():
    def __init__(self):
        self.mutex = Lock()
        self.eating = Value('i',0) # 1 <= eating <= 2
        self.other_eating = Condition(self.mutex)
    
    def is_eating(self, num):
        self.mutex.acquire()
        self.eating.value += 1
        self.other_eating.notify_all()
        self.mutex.release()
        
    def cond_think(self):
        return self.eating.value > 1
        
    def wants_think(self, num):
        self.mutex.acquire()
        self.other_eating.wait_for(self.cond_think, 0.5)
        self.eating.value -= 1
        self.mutex.release()
        
        
class AnticheatTable():
    def __init__(self, size: int, manager):
        self.phil = None
        self.size = size
        self.hungry = manager.list([False]*self.size)
        self.fork = manager.list([False]*self.size)
        self.mutex = Lock()
        self.can_eat = Condition(self.mutex)
        self.chungry = Condition(self.mutex)

    def have_fork(self):
        return not(self.fork[(self.phil-1)%self.size] or self.fork[(self.phil+1)%self.size])
    def no_hungry(self):
        return not self.hungry[(self.phil + 1)%self.size]
    
    def set_current_phil(self,num):
        self.phil = num  
    
    def wants_eat(self, num):
        self.mutex.acquire()
        self.chungry.wait_for(self.no_hungry)
        self.hungry[num] = True
        self.can_eat.wait_for(self.have_fork)
        self.fork[num] = True
        self.hungry[num] = False
        self.chungry.notify_all()
        self.mutex.release()

    def wants_think(self, num):
        self.mutex.acquire()
        self.fork[num] = False
        self.can_eat.notify_all()
        self.mutex.release()

        
        
        
        
        
        
        
        
        
        
        
        

   

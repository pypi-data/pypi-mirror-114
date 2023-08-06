#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################
## Reynan Br. ##
## 23 de Jul  ##
## 12:42      ##
################

def prod(*args:float)-> float:
   res = list(args)[0]
   for i in range(len(args)-1):
       res *= args[i+1]
   return res
    
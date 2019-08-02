# -*- coding: utf-8 -*-

    3 #--------------------------------------------------------------------#
    4 #                                                                    #
    5 # Copyright (C) 2018 HOLOEYE Photonics AG. All rights reserved.      #
    6 # Contact: https://holoeye.com/contact/                              #
    7 #                                                                    #
    8 # This file is part of HOLOEYE SLM Display SDK.                      #
    9 #                                                                    #
   10 # You may use this file under the terms and conditions of the        #
   11 # "HOLOEYE SLM Display SDK Standard License v1.0" license agreement. #
   12 #                                                                    #
   13 #--------------------------------------------------------------------#
   14 
   15 
   16 
   17 
# Import the SLM Display SDK:
import detect_heds_module_path
from holoeye import slmdisplaysdk
   21 
   22 
# Function to print some statistics:
def printStat(stat, dataHandles):
    sum = 0.0
    count = 0
    min = 10000
    max = -10000
   29 
    for handle in dataHandles:
    # get the stat from the handle
        v = getattr(handle, stat)
   33 
        # check if this action did happen at all
    if v == slmdisplaysdk.Datahandle.NotDone:
        continue
   37 
    # process value
        sum += float(v)
        count += 1
   41 
        if v < min:
        min = v
   44 
        if v > max:
        max = v
   47 
    # check if any handle did this action
    if count > 0:
        avg = sum / count
   51 
    print("{0:<16} -> min: {1:<3}  -  avg: {2:<3}  -  max: {3:<3}".format(stat, min, avg, max))
    else:
    print("{0:<16} -> min: {1}  -  avg: {1}  -  max: {1}".format(stat, "n/a"))

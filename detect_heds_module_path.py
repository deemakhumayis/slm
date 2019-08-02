1 # -*- coding: utf-8 -*-
2 
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
16 #--------------------------------------------------------------------#
17 #                                                                    #
18 # Copyright (C) 2018 HOLOEYE Photonics AG. All rights reserved.      #
19 # Contact: https://holoeye.com/contact/                              #
20 #                                                                    #
21 # This file is part of HOLOEYE SLM Display SDK.                      #
22 #                                                                    #
23 # You may use this file under the terms and conditions of the        #
24 # "HOLOEYE SLM Display SDK Standard License v1.0" license agreement. #
25 #                                                                    #
26 #--------------------------------------------------------------------#
27 
28 
29 # Please import this file in your scripts before actually importing the HOLOEYE SLM Display SDK,
30 # i. e. copy this file to your project and use this code in your scripts:
31 #
32 # import detect_heds_module_path
33 # import holoeye
34 #
35 #
36 # Another option is to copy the holoeye module directory into your project and import by only using
37 # import holoeye
38 # This way, code completion etc. might work better.
39 
40 
import os, sys
 
# Import the SLM Display SDK:
HEDSModulePath = os.getenv("HEDS_PYTHON_MODULES", "")
print("HEDSModulePath = " + HEDSModulePath)
if HEDSModulePath == "":
    print('\033[91m' + "\nError: Could not find HOLOEYE SLM Display SDK installation path from environment variable. \n\nPlease relogin your Windows user account and try again. \nIf that does not help, please reinstall the SDK and then relogin your user account and try again. \nA simple restart of the computer might fix the problem, too." + '\033[0m')
    sys.exit(1)
sys.path.append(HEDSModulePath)

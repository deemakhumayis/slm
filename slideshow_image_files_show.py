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
   16 # Plays a slideshow on the SLM using image files from a single folder.
   17 # The image files are shown directly on the SLM as soon as the data was transmitted,
   18 # using the API function showDataFromFile().
   19 # The duration each image is shown can be configured and is maintained by simple sleep commands.
   20 # For holograms, please use image formats which are uncompressed (e.g. BMP) or which use lossless compression, like PNG.
   21 
   22 import os, sys, time, math
   23 
   24 # Import the SLM Display SDK:
   25 import detect_heds_module_path
   26 from holoeye import slmdisplaysdk
   27 
   28 # Make some enumerations available locally to avoid too much code:
   29 ErrorCode = slmdisplaysdk.SLMDisplay.ErrorCode
   30 ShowFlags = slmdisplaysdk.SLMDisplay.ShowFlags
   31 
   32 # Detect SLMs and open a window on the selected SLM:
   33 slm = slmdisplaysdk.SLMDisplay()
   34 
   35 # Open the SLM preview window (might have an impact on performance):
   36 slm.utilsSLMPreviewShow()
   37 
   38 # Configure slideshow:
   39 imageFolder = "C:/Users/Public/Pictures/Sample Pictures"  # please enter a valid folder path
   40 imageDisplayDurationMilliSec = 2000  # please select the duration in ms each image file shall be shown on the SLM
   41 repeatSlideshow = 3  # <= 0 (e. g. -1) repeats until Python process gets killed
   42 
   43 # Please select how to scale and transform image files while displaying:
   44 displayOptions = ShowFlags.PresentAutomatic  # PresentAutomatic == 0 (default)
   45 #displayOptions |= ShowFlags.TransposeData
   46 #displayOptions |= ShowFlags.PresentTiledCentered  # This makes much sense for holographic images
   47 displayOptions |= ShowFlags.PresentFitWithBars
   48 #displayOptions |= ShowFlags.PresentFitNoBars
   49 #displayOptions |= ShowFlags.PresentFitScreen
   50 
   51 # Search image files in given folder:
   52 filesList = os.listdir(imageFolder)
   53 
   54 # Filter *.png, *.bmp, *.gif, and *.jpg files:
   55 imagesList = [filename for filename in filesList if str(filename).endswith(".png") or str(filename).endswith(".gif") or str(filename).endswith(".bmp") or str(filename).endswith(".jpg")]
   56 
   57 print(imagesList)
   58 
   59 print("Number of images found in imageFolder = " + str(len(imagesList)))
   60 
   61 if len(imagesList) <= 0:
   62     sys.exit()
   63 
   64 # Save the start time:
   65 avgFPSStartTime = time.time()
   66 currentFPSStartTime = avgFPSStartTime
   67 
   68 # Play complete slideshow:
   69 n = 0
   70 while (n < repeatSlideshow) or (repeatSlideshow <= 0):
   71     n += 1
   72 
   73     #Play slideshow once:
   74     for i, filename in enumerate(imagesList):
   75         # Measure time between images and duration of current image:
   76         currentFPSStartTime = time.time()
   77 
   78         filepath = os.path.join(imageFolder, filename)
   79 
   80         # Show image on SLM. Function returns after image was loaded and displayed:
   81         error = slm.showDataFromFile(filepath, displayOptions)
   82         assert error == ErrorCode.NoError, slm.errorString(error)
   83         passedTime = time.time() - currentFPSStartTime
   84 
   85         # Wait for next image. Wait rest of desired time after slm.showDataFromFile() took some time already:
   86         sleep_duration = float(imageDisplayDurationMilliSec)/1000.0 - passedTime
   87         if (sleep_duration > 0.0):
   88             time.sleep(sleep_duration)
   89 
   90         outputStr = "n = " + str("%3d" % n)
   91 
   92         # Show actual current frames per seconds:
   93         delta_t = time.time() - currentFPSStartTime
   94         fps = 1.0 / delta_t
   95         outputStr += "   FPS = " + str("%5.2f" % fps)
   96 
   97         outputStr += "   file number = " + str("%5d" % (i+1))
   98         outputStr += "   file name: " + str(filename)
   99 
  100         print(outputStr)
  101 
  102 # Show a blank screen with gray value 128 as last image:
  103 error = slm.showBlankscreen(128)
  104 assert error == ErrorCode.NoError, slm.errorString(error)
  105 
  106 # Wait a few seconds after the slideshow has finished:
  107 time.sleep(4)
  108 
  109 # Unloading the SDK may or may not be required depending on your IDE:
  110 slm.release()

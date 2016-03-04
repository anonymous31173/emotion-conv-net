import os, shutil, sys, time, re, glob
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import Image
import caffe

from caffe_functions import *
from opencv_functions import *
from utility_functions import *


################################################################################################
#
# TO DO:
#  - Running average to smooth out fluctuations in face detection and emotion classification
#  - Test accuracy of different networks
#  - Consider downloading and training a brand new network 
#    The paper Chris sent us got 95% accuracy training an SVM on top of GoogLeNet!
#  - Improve speed if at all possible
#  - Embed on the TK1! (you got this, Chris)
#
#################################################################################################

categories = [ 'Angry' , 'Disgust' , 'Fear' , 'Happy'  , 'Neutral' ,  'Sad' , 'Surprise']

# Set up face detection
faceCascades = load_cascades()

# Set up network
mean = None
VGG_S_Net = make_net(mean)

# Get all emojis
emojis = loadAllEmojis()


# Set up display window
cv.namedWindow("preview")

# Open input video steam
vc = cv.VideoCapture(0)

# Check that video stream is running
if vc.isOpened(): # try to get the first frame
  rval, frame = vc.read()
  #frame = frame.astype(np.float32)
else:
  rval = False


while rval:
  # Mirror image
  frame = np.fliplr(frame)
  
  # Detect faces
  detect = True
  if detect:
    # Find all faces
    _, faces = DetectFace(frame,True,faceCascades,single_face=False,second_pass=False,draw_rects=False)
    #frame = addEmoji(frame,faces,emoji)

    if len(faces) == 0 or faces is None:
      # No faces found
      pass
    else:
      # Toggle whether to do dynamic classification, or just to display one user-picked emoji
      useCNN = True

      if useCNN:
        # Get a label for each face
        labels = classify_video_frame(frame, faces, VGG_S_Net, categories=None)

        # Add an emoji for each label
        frame = addMultipleEmojis(frame,faces,emojis,labels)
        
        # Print first emotion detected
        print categories[labels[0]]

      else:
        # Just use the smiley face (no CNN classification)
        categoryIndex = 3  # Choose the index of the emotion category you wish to display (3=happy)
        frame = addEmoji(frame,faces,emojis[categoryIndex])

  # Show video with faces
  cv.imshow("preview", frame)


  # Read in next frame
  rval, frame = vc.read()

  # Wait for user to press key. On ESC, close program
  key = cv.waitKey(20)
  if key == 27: # exit on ESC
    break

cv.destroyWindow("preview")
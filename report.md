###FINAL YEAR PROJECT
####MAYNOOTH UNIVERSITY
##ALEXANDER MITCHELL
####12327311
###Development of an Asynchronous Stereo Vision Technique to be Implemented in a Visual Radar Tracking System

##1.Abstract

##2.Introduction
introduction to the addressed topic:
The topic being addressed by this project is stereo computer vision, the use of 2 cameras to get information in a 3D environment. My project specifically focuses on the implementation of an asynchronous technique.

motivation, why people should care, what are you trying to achieve:
In a typical stereo vision setup, the assumption is made that each camera is taking photos at the same time. This cannot be the case in a single threaded application. My project avoids this assumption by taking photos asynchronously(at different times).

technical description of problem:
In typical synchronous stereo vision, 2 photographs of an object can be taken at the same time. The difference can be used to calculate depth information. Another set of 2 photos can be taken to get the location at a second point in time and then work out the velocity of the object. The problem I am trying to solve is taking 4 photos at different times and calculate velocity in one go. The photos must be taken as fast as possible to make sure the entity does not change direction.
summary of how project was approached:

how to evaluate work
describe achievements

##3.Technical Background
- research into synchronous stereo vision
- xbox 360 kinect sensor
- xbox one kinect sensor

- lack of research in asychronous stereo vision

- docs.opencv.org

##4.The Problem
- describe synchronous stereo vision
- describe assumptions made with stereo vision
- describe front and parallel cameras
- finding the same object in both cameras
- calculating the intrinsic parameters

In traditional stereo vision, 2 cameras, A and B, are set up front and parallel. The distance between the cameras is measured and called the baseline, b. Some intrinsic parameters are also required. 2 identical cameras should be used in any stereo vision technique to avoid complications in further calculations. The focal length and and size of the imaging sensor for the cameras are required. Knowing the size and resolution of the image plane allows us to translate between pixels and millimeters for the results.

Once the cameras are set up as described above, A photo is taken with each camera at the same time. Next the object must be located in both images. X-Y coordinates in pixels are used to describe the location of the object in the image. The interesting measurement is the Z coordinate, or depth.

Z=f*b/d

In a typical synchronous stereo vision technique, the assumption is made that the cameras can take pictures at the same time. This is not true in a single threaded application where only one camera can be controlled at a time. This can be demonstrated with pseudo code:

frame1 = capL.read()
frame2 = capR.read()

There will always be a time delay between each line of code being executed.

Most stereo vision techniques make the assumption that the cameras are pointing front and parallel. The alignment of the cameras is a big factor in the accuracy of the photos being taken, especially at long distances. Having the cameras perfectly aligned is an important problem to solve.



##5.The Solution

##6.Evaluation

##7.Conclusions

##8.References

##9.Appendices

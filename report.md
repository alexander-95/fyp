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

lack of research in asychronous stereo vision

- docs.opencv.org
- 

##4.The Problem

##5.The Solution

##6.Evaluation

##7.Conclusions

##8.References

##9.Appendices


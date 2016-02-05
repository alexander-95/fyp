###FINAL YEAR PROJECT
####MAYNOOTH UNIVERSITY
##ALEXANDER MITCHELL
####12327311
###Development of an Asynchronous Stereo Vision Technique to be Implemented in a Visual Radar Tracking System

\pagebreak

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

```python
Z=f*b/d  
```

In a typical synchronous stereo vision technique, the assumption is made that the cameras can take pictures at the same time. This is not true in a single threaded application where only one camera can be controlled at a time. This can be demonstrated with pseudo code:  
```python
frame1 = capL.read()  
frame2 = capR.read()  
```

There will always be a time delay between each line of code being executed.  

Most stereo vision techniques make the assumption that the cameras are pointing front and parallel. The alignment of the cameras is a big factor in the accuracy of the photos being taken, especially at long distances. Having the cameras perfectly aligned is an important problem to solve.  

In a scene that has many features, it can be hard to locate the object of interest. In order to track an object, the same feature point must be recognised from both cameras. There is also the problem of getting multiple matches in feature recognition. The next decision would be what entity to track.  

I will need to know the intrinsic parameters of the cameras that I will be using. Firstly, I will need to know the focal length of the cameras since it's one of the key variables in the triangulation process. I will also need to know how big the camera sensor is and the dimensions of a pixel. The only unit of measurement I will have for the images I take, is pixels whereas any measurements in the outside world will be taken in millimeters. Finding the size of a single pixel will allow me to convert between the two units of measurement.  

##5.The Solution
ANALYTICAL WORK
Since this project is a continuation of a previous project, I will be reusing mathematical formulae that have been used by Colm O Connell. The method I will be using, takes 4 photos at different times, t1, t2, t3 and t4. The location of the object can be calculated at t1 and t4:  

- position at time 1:
```python
X1 = (((-1)*b*f)/(d2-d1)) + ((t2 - t1)*(f*Vy - Vx*d2))/(d2-d1)  
Y1 = ( ((d1*(t2 - t1)*Vy) - d1*b)/(d2-d1)) - ((d1*d2*Vx*(t2 - t1))/(f*(d2-d1)))  
Z1 = X1*(dz1/f)  
```

- position at time 4:
```python
X4 = (f*b/(d3-d4)) + (((t4 - t3)*(Vx*d3 - Vy*f))/(d3-d4))  
Y4 = (((b*d3)-(d4*(t4 - t3)*Vy))/(d3-d4)) + (((t4 - t3)*Vx*d4*d3)/(f*(d3-d4)))  
Z4 = X4*(dz4/f)  
```
- b = baseline  
- f = focal length  
- d1, d2, d3, d4 = disparity in x direction in photo taken at t1, t2, t3 and t4 respectively.  
- dz1, dz2, dz3, dz4 = disparity in y direction in photo taken at t1, t2, t3, t4 respectively.  
- t1, t2, t3, t4 = time at which img1, img2, img3 and img4 were taken at respectively.  
- (x1, y1), (x1, y1), (x1, y1), (x1, y1) = pixel coordinates of point of interest in photo taken at t1, t2, t3 and t4 respectively.  

- some extra variables
```python
z1 = x1*(dz1/f)  
z2 = x2*(dz2/f)  
Vz = (z2 - z1)/(t2 - t1)  

num = (A*b*(d2-d4))+(C*b*(d3-d1))  
denom = (C*((t2 - t1)*(d3-d1)-(t3 - t1)*(d2-d1))) + (A*((t4 - t3)*(d2-d4)-(t4 - t2)*(d3-d4)))  
Vy = num/denom  

num = (f*b*(d2-d4)) - ((t4 - t3)*f*Vy*(d2-d4)) + ((t4 - t2)*f*Vy*(d3-d4))  
denom = (t4 - t2)*d2*(d3-d4) - (t4 - t3)*d3*(d2-d4)  
Vx = num/denom  

A = ((t2 - t1)*d2*(d3-d1)) - ((t3 - t1)*d3*(d2-d1))  
C = ((t4 - t2)*d2*(d2-d4)) - ((t4 - t3)*d3*(d3-d4))  
```

DIAGRAM AND EXPLANATION OF CAMERA SETUP  
HIGH LEVEL DESIGN  
To make the images easier to analyse, I will be taking photos of a dark target against a light background, or vice versa.
The photos will be converted to greyscale and thresholded. The time at which the photos were taken will be recorded and the location of the object in the image using blob detection. Noise reduction may be necessary in places to smooth out the image. Most of the image manipulation will be done using python opencv.

LOW LEVEL DESIGN  
- convert color  
- gaussian blur  
- threshold  
- centroid  
- getMetrics   

IMPLEMENTATION  
- anything else of interest
  + move onto bigger things: track an aircraft.
  + run experiment to test limits of the program.
  + NTP ip cameras
  + build rig for mounting cameras
  + mention trade-off between FOV and accuracy,(diluting the pixels)

##6.Evaluation
- SOLUTION VERIFICATION
For the purpose of verifying the validity of my project, I positioned an object at set locations and compared it against the output of my program.  
[insert diagram here]  
The above diagram shows how the object moves along a diagonal line at set intervals. This is to simulate constant velocity. The x and z coordinates are clear from the diagram. The y coordinate can be calculated using images from the camera. The y coordinate should be constant since the object is moving along the floor. The following diagram shows how the y position can be calculated:  
[insert diagram here]  

- SOFTWARE DESIGN VERIFICATION
  + show how centroids were found (vision notes)
  + show how to count the number of objects in the scene
  + show how cameras were aligned (and maybe stereo calibration)
  + UML diagrams of how main method works
- SOFTWARE VERIFICATION
  + how to perform a table top experiment using predefined pictures and predefined timestamps.
- VALIDATION/MEASUREMENTS

##7.Conclusions
- implications of my work
- contribution to the state of the art
- discuss whether results are general, potentially generalised or specific to a particular case
- identify threats to the validity of results(limitations and risks)
- Discuss approach (probably irrelevant?)
- Discuss future work

The asynchronous stereo vision technique that is used in this project removes the epipolar geometry. This means that the cameras don't have to be looking at the same scene. This allows the cameras to be spaced further apart. A larger baseline gives greater accuracy for objects further away.  

The asynchronous technique, by definition, means that the cameras don't have to be synchronised. This means that they don't have to be connected to the same machine. This can open up doors to using distributed cameras to track objects.  

The technique used in this project could be interpreted as an intersection of planes problem. A vector can be created from the camera to the object at 2 different times. As long as the object moves, the vectors will not be parallel. This allows us to create a plane which both vectors sit on. Another pair of vectors and a plane can be produced using the second camera. The intersection of these 2 planes can be used to represent the trajectory of the object. This allows the use of simpler matrix operations instead of a geometric approach.  


The main limitation to the approach that I've taken is that the object is assumed to have constant velocity. This means that the object moves in a straight line and at a constant speed. In the interest of accuracy, The time between images being taken is minimised to   

##8.References
- list of cited work(IEEE guidelines)

##9.Appendices
- source code
- project management
- significant deviations from plan
- things to do differently if done again

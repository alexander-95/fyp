###FINAL YEAR PROJECT
####MAYNOOTH UNIVERSITY
##ALEXANDER MITCHELL
####12327311
###Development of an Asynchronous Stereo Vision Technique to be Implemented in a Visual Radar Tracking System

\pagebreak

##1.Abstract
Get on with it

\pagebreak

##2.Introduction
introduction to the addressed topic:  
The topic being addressed by this project is stereo computer vision, the use of two cameras to get information in a 3D environment. My project specifically focuses on the implementation of an asynchronous technique. This allows to cameras to be set up in different locations whereas a more traditional setup requires the cameras to be side by side.  

motivation, why people should care, what are you trying to achieve:  
A typical stereo vision sensor has two sensors built into the one unit, like the xbox kinect. My technique will allow the use of two independent cameras such as two people pointing smartphone cameras at the same time. If the cameras can send information back to a central source, the location of an object can be calculated.  

technical description of problem:  
In typical synchronous stereo vision, two photographs of an object can be taken at the same time. The difference in the images can be used to calculate depth information. Another set of two photos can be taken to get the location at a second point in time and then work out the velocity of the object. The problem I am trying to solve is taking four photos at different times and calculate velocity in one go. The first camera takes the first two images, then the second camera takes the third and fourth images. It is assumed that the object travels with constant velocity. This may mean taking the pictures as fast as possible to make sure the velocity doesn't change.  

summary of how project was approached:

how to evaluate work
describe achievements

\pagebreak

##3.Technical Background
- what to do here?

- lack of research in asychronous stereo vision
existing solutions - There are only existing solutions using synchronised cameras such as the xbox kinect.

- docs.opencv.org


\pagebreak

##4.The Problem
- describe synchronous stereo vision
- describe assumptions made with stereo vision
- describe front and parallel cameras
- finding the same object in both cameras
- calculating the intrinsic parameters

In traditional stereo vision, two cameras, A and B, are set up front and parallel. The distance between the cameras is measured and called the baseline, b. Some intrinsic parameters are also required. two identical cameras should be used in any stereo vision technique to avoid complications in further calculations. The focal length and and size of the imaging sensor for the cameras are required. Knowing the size and resolution of the image plane allows us to translate between pixels and millimeters for the results.  
[insert diagram here for typical stereo vision setup]  
Once the cameras are set up as described above, A photo is taken with each camera at the same time. Next the object must be located in both images. X-Y coordinates in pixels are used to describe the location of the object in the image. The interesting measurement is the Z coordinate, or depth.  

```python
Z=f*b/d  
```

Most stereo vision techniques make the assumption that the cameras are pointing front and parallel. The alignment of the cameras is a big factor in the accuracy of the photos being taken, especially at long distances. Having the cameras perfectly aligned is an important problem to solve.  

In a scene that has many features, it can be hard to locate the object of interest. In order to track an object, the same feature point must be recognised from both cameras. There is also the problem of getting multiple matches in feature recognition. The next decision would be what entity to track.  

I will need to know the intrinsic parameters of the cameras that I will be using. Firstly, I will need to know the focal length of the cameras since it's one of the key variables in the triangulation process. I will also need to know how big the camera sensor is and the dimensions of a pixel. The only unit of measurement I will have for the images I take, is pixels whereas any measurements in the outside world will be taken in millimeters. Finding the size of a single pixel will allow me to convert between the two units of measurement.  

\pagebreak

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
```
```python
num = (A*b*(d2-d4))+(C*b*(d3-d1))  
denom = (C*((t2 - t1)*(d3-d1)-(t3 - t1)*(d2-d1))) + (A*((t4 - t3)*(d2-d4)-(t4 - t2)*(d3-d4)))  
Vy = num/denom  
```
```python
num = (f*b*(d2-d4)) - ((t4 - t3)*f*Vy*(d2-d4)) + ((t4 - t2)*f*Vy*(d3-d4))  
denom = (t4 - t2)*d2*(d3-d4) - (t4 - t3)*d3*(d2-d4)  
Vx = num/denom  
```
```python
A = ((t2 - t1)*d2*(d3-d1)) - ((t3 - t1)*d3*(d2-d1))  
C = ((t4 - t2)*d2*(d2-d4)) - ((t4 - t3)*d3*(d3-d4))  
```

######DIAGRAM AND EXPLANATION OF CAMERA SETUP  
######HIGH LEVEL DESIGN  
To make the images easier to analyse, I will be taking photos of a dark target against a light background, or vice versa.
The photos will be converted to greyscale and thresholded. The time at which the photos were taken will be recorded and the location of the object in the image using blob detection. Noise reduction may be necessary in places to smooth out the image. Most of the image manipulation will be done using Python and OpenCV.

######LOW LEVEL DESIGN
- convert color (make the image grayscale)
- gaussian blur (noise reduction)
- threshold (increase contrast)
- find centroid (first order moment)
- getMetrics (function for stereo vision calculations)

######IMPLEMENTATION  
- anything else of interest
  + move onto bigger things: track an aircraft.
  + run experiment to test limits of the program.
  + NTP ip cameras
  + build rig for mounting cameras
  + mention trade-off between FOV and accuracy,(diluting the pixels)

  solve problem using vectors and planes
  - camera1 has 2 vectors pointing at t1 and t2 respectively
  - camera2 has 2 vectors pointing at t3 and t4 respectively
  - vectors t1 and t2 lie on the plane p1
  - vectors t3 and t4 lie on the plane p2

find the cross product between t1 and t2. This is the normal vector n1 to the plane p1
use the normal vector to get the equation of the plane.

repeat the process for the second plane.
Use a system of linear equations to find the intersection between the 2 planes. This is the trajectory of the object. 

\pagebreak

##6.Evaluation
######SOLUTION VERIFICATION
For the purpose of verifying the validity of my project, I positioned an object at set locations and compared it against the output of my program.  
[insert diagram here]  
The above diagram shows how the object moves along a diagonal line at set intervals. This is to simulate constant velocity. The x and z coordinates are clear from the diagram. The y coordinate can be calculated using images from the camera. The y coordinate should be constant since the object is moving along the floor. The following diagram shows how the y position can be calculated:  
[insert diagram here]  

######SOFTWARE DESIGN VERIFICATION
+ show how centroids were found (vision notes)
+ show how to count the number of objects in the scene
+ show how cameras were aligned (and maybe stereo calibration)
+ UML diagrams of how main method works

######SOFTWARE VERIFICATION
+ how to perform a table top experiment using predefined pictures and predefined timestamps.  (Are soluation and software verification the same thing?)

######VALIDATION/MEASUREMENTS
+ measuring objects at a known distance

\pagebreak

##7.Conclusions
- implications of my work
- contribution to the state of the art
- discuss whether results are general, potentially generalised or specific to a particular case
- identify threats to the validity of results(limitations and risks)
- Discuss approach (probably irrelevant?)
- Discuss future work

######IMPLICATIONS  
The asynchronous stereo vision technique that is used in this project removes the epipolar geometry. This means that the cameras don't have to be looking at the same scene. This allows the cameras to be spaced further apart. A larger baseline gives greater accuracy for objects further away.  

The asynchronous technique, by definition, means that the cameras don't have to be synchronised. This means that they don't have to be connected to the same machine. This can open up doors to using distributed cameras to track objects.  

######CONTRIBUTION  
The technique used in this project could be interpreted as an intersection of planes problem. A vector can be created from the camera to the object at 2 different times. As long as the object moves, the vectors will not be parallel. This allows us to create a plane which both vectors sit on. Another pair of vectors and a plane can be produced using the second camera. The intersection of these 2 planes can be used to represent the trajectory of the object. This allows the use of simpler matrix operations instead of a geometric approach.  

######LIMITATIONS  
The main limitation to the approach that I've taken is that the object is assumed to have constant velocity. This means that the object moves in a straight line and at a constant speed. In the interest of accuracy, The time between images being taken is minimised to overcome this limitation.  

Using my current setup, I can only identify an object, if it is the only object in the scene. I have not implemented any other recognition features. This could cause problems if the cameras are looking at a target from different viewpoints. This is a potential limitation for an intersection of planes method which relies on different viewpoints.  

######FUTURE WORK  
- track multiple targets
- track using independent cameras
- Use more robust recognition

A good move forward would be to track multiple objects at the same time. This would involve an intelligent way of mapping objects from one scene to the next.

Another advancement could be to use cameras with different orientations. In my current setup, I have cameras that are front and parallel. This simplifies calculations since the yaw, pitch and roll of the cameras are equal. This means that such variables can be disregarded from the calculations. By taking these variables into account, the cameras could be set up at different orientations. Complexity is added by having to work out the extra angles. Smartphones have all the capabilities to track position using GPS and orientation using a compass and gyroscope. By using the intersection of planes method, an object could be tracked using two smartphones pointing at the target from 2 different viewpoints.

\pagebreak

##8.References
- list of cited work(IEEE guidelines)

\pagebreak

##9.Appendices
- source code
- project management
- significant deviations from plan
- things to do differently if done again

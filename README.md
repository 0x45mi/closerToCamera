## Closer to camera

### Description

Animate the depth of an object in camera space. <br />
Intended as a tweaker tool for later anim stages where timings have been established.

It works best by selecting one controller as the target. The tool supports multi-controller selections by calculating the mid point of the controllers.<br />

If you see the bake is not working well, there is a right click option called "layers". This option will make the bake a bit slower but it should be accurate.<br />

[Ckeck out the tool's video tutorial](https://vimeo.com/765705742)
### Installation

Copy the script file into your maya scripts directory, for example:<br />
_C:\Users\YourUser\Documents\maya\scripts\emi_closerToCamera.py_
 
Run the tool in a python shell or shelf button by importing the module, 
and then calling the primary function:
```
import emi_closerToCamera
emi_closerToCamera.ui()
```

 

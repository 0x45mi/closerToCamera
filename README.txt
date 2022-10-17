   __________________
__/__ Description __/__
 
Animate the depth of an object in camera space.
Although the tool is called "Closer to camera", untruthfully to it's name, you can also animate objects going further away.
Intended as a tweaker tool for later anim stages where timings have been established.

It works best by selecting one controller as the target. However, the tool supports multi-controller selections by calculating the mid point of the controllers.

   ___________________
__/__ Installation __/__
 
Copy the script file into your maya scripts directory, for example:
C:\Users\YourUser\Documents\maya\scripts\emi_closerToCamera.py
 
Run the tool in a python shell or shelf button by importing the module, 
and then calling the primary function:
 
import emi_closerToCamera
emi_closerToCamera.ui()

   ____________
__/__License__/__

Copyright 2022 Emily Lim Sarrias

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Python Particle Simulation
### A project to introduce myself to Python

I've used some basic mechanics to implement a small simulator for 2D circle elastic collisions. The collision function conserves momentum and energy for a realistic aesthetic. 

## The Process
The most difficult issue, unrelated to familiarizing myself with the Python language, was producing collisions that did not cause glitchy  effects. I'll explain an example of a hacky, unrefined solution that I first implemented, and then I'll show a more elegant solution. 

**Firstly**, There is an obvious condition that must be met in order for a collision to occur. The condition is that two balls must be overlapping. To quantize this condition, we need a couple bits of information about each ball.
1. The radius
2. The center position (x,y)
\
\
Two conditions must be met for an actual **collision** to occur.
1. The balls must be overlapping.
2. The distance between the two balls must be decreasing.



## Author:
 Bailey Lind-Trefts

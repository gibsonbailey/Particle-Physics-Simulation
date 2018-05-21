# Python Particle Simulation
### A project to introduce myself to Python

I've used some basic mechanics to implement a small simulator for 2D circle elastic collisions. The collision function conserves momentum and energy for a realistic aesthetic. 

## The Process
The most difficult issue, unrelated to familiarizing myself with the Python language, was producing collisions that did not cause glitchy  effects. I'll explain an example of a hacky, unrefined solution that I first implemented, and then I'll show a more elegant solution. 
<br/>
<br/>
### Firstly
There is an obvious condition that must be met in order for a collision to occur: two balls must be overlapping. To define this condition, we need a couple bits of information about each ball.
1. The radius
2. The center position (x,y)
<br/>
The ball class is built to store each of these fields, so we have easy access to them. We can use the center positions of each ball to calculate the distance between the two of them. The general distance formula for two dimensions is shown below.

![2-D distance formula](distance_formula.png?s=200)

<br/>
<br/>
Two conditions must be met for an actual **collision** to occur.
1. The balls must be overlapping.
2. The distance between the two balls must be decreasing.



## Author:
 Bailey Lind-Trefts

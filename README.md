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
<br/>
<br/>
<img src="distance_formula.png" width="25%">
<br/>
In the real world, this is the only condition that would actually need to be met, since real time is continuous. However, the time in this program is discretized, and a problem emerges from this distinction.
<br/>
<br/>
Inside the ball class is an elasticity value that determines the portion of momentum conserved from each collision. If this elasticity value is less than one (for artificial entropy), then balls continually meet the overlapping condition. For example, two balls may fly at each other directly (along the same line). There will be an instance in time in the program that the balls of equal mass meet the overlapping condition. Due to this condition being met, the collision function continues, and the velocities of the two balls are swapped due to each ball having an equivalent mass. Not only are these balls' velocities swapped, but they are each multiplied by the elasticity constant which causes each velocity to be decreased slightly.
<br/>
<br/>
The next time that the simulation loop moves the balls a distance corresponding to one time step, the distance between the two centers will increase. However, since each of the velocities were decreased slighly by the lack of elasticity, it is not unlikely that the balls will still be overlapping, which causes the collision function to be called again. This is what I refer to as the "sticky ball" problem, and it completely ruins the effect of bouncing balls.
<br/>
<br/>
### An Elegant Solution
Two conditions must be met for an actual **collision** to occur.
1. The balls must be overlapping.
2. The distance between the two balls must be decreasing.



## Author:
 Bailey Lind-Trefts

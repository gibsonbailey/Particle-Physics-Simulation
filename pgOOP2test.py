import pygame
import sys
import random
import math
import time
import os

###### Pygame Window ######
screenwidth = 1350
screenheight = 750


screen = pygame.display.set_mode((screenwidth,screenheight),pygame.FULLSCREEN)
print(pygame.display.list_modes())


###### Ball Attributes ######
# Spawns balls with mostly tangential velocity for semi-circular orbits
BALL_TANGENTIAL_INITIAL_VELOCITY = True

# Number of balls initially spawned
BALLQUANTITY = 35

# Parameters for ball size
BALLMINRADIUS = 5
BALLMAXRADIUS = 20

# Initial ball speed parameters
BALLMAXVELOCTY = 100

# Controls how spread out the balls will spawn
INITALBALLSPREAD = 70



###### Time Attributes ######
# Controls the time scale at which the simulation operates
TIMESPEED = 1.5



###### Gravity Field Controls ######
# Uniform Gravity Field or Centralized Gravity Field
G_NONUNIFORM = True

# Acceleration due to gravity (Uniform Gravity Field)
acc_g = 0.2

# Nonuniform Gravity Field
G_CENTER_X = screenwidth / 2
G_CENTER_Y = screenheight / 2
G_MAGNITUDE = 700

# For large central particle (Star)
STAR_PARTICLE = True
DRAG_COEFFICIENT = 4



###### Collisions ######
# Particle collisions with the walls of the pygame window
BOUNDS = False

# Collisions between particles themselves
PARTICLE_COLLISIONS = False


###### Colors ######
BLACK = (0,0,0)



#Primary particle of the simulation
class ball:

    # Buffer between screen edges and balls
    x_padding = 5
    y_padding = 5

    # Collision dampening (less elasticity is more dampening)
    elasticity = 0.9

    # Constructor
    def __init__(self,x,y,r):
        self.radius = r
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.mass = self.radius * self.radius # scales with area of the ball

        # center position of ball on screen
        self.x = x
        self.y = y

        if BALL_TANGENTIAL_INITIAL_VELOCITY:
            self.dx = self.x - G_CENTER_X
            self.dy = self.y - G_CENTER_Y
            self.angle_p = math.atan2(-self.dy,-self.dx)

            # For small noise in the start angle (for elliptical orbits)
            self.angle_dev = random.uniform(-0.5,0.5)
            self.angle_p += self.angle_dev

            # Initial velocity magnitude
            self.speed = random.uniform(-BALLMAXVELOCTY,BALLMAXVELOCTY)

            self.v_x = self.speed * math.cos(self.angle_p - (math.pi/2))
            self.v_y = self.speed * math.sin(self.angle_p - (math.pi/2))
        else:
            self.v_x = random.uniform(-BALLMAXVELOCTY,BALLMAXVELOCTY)
            self.v_y = random.uniform(-BALLMAXVELOCTY,BALLMAXVELOCTY)

        if G_NONUNIFORM == False:
            self.a_x = 0.0
            self.a_y = acc_g
        else:
            self.dx = self.x - G_CENTER_X
            self.dy = self.y - G_CENTER_Y
            self.center_dist = math.hypot(self.dx,self.dy)
            self.acc_g = G_MAGNITUDE / math.pow(self.center_dist,0.8)
            self.theta_ball = math.atan2(self.dy,self.dx)
            self.drag = DRAG_COEFFICIENT * math.pow(math.hypot(self.v_x,self.v_y),1) + 5
            self.a_x = self.acc_g * math.cos(self.theta_ball + math.pi)
            self.a_y = self.acc_g * math.sin(self.theta_ball + math.pi)


    # Updates the position of the ball
    def move(self, deltaT):
        deltaT *= TIMESPEED / 1000
        if BOUNDS:
            if((self.x >= screenwidth - self.radius - ball.x_padding and self.v_x > 0.0) or (self.x <= 0 + self.radius + ball.x_padding and self.v_x < 0)):
                self.v_x = -self.v_x * ball.elasticity
            if((self.y >= screenheight - self.radius - ball.y_padding and self.v_y > 0.0) or (self.y <= 0 + self.radius + ball.y_padding and self.v_y < 0)):
                self.v_y = -self.v_y * ball.elasticity

        if G_NONUNIFORM:
            self.dx = self.x - G_CENTER_X
            self.dy = self.y - G_CENTER_Y
            self.center_dist = math.hypot(self.dx,self.dy)
            self.acc_g = G_MAGNITUDE / math.pow(self.center_dist,0.8)
            self.theta_ball = math.atan2(self.dy,self.dx)
            self.a_x = self.acc_g * math.cos(self.theta_ball + math.pi)
            self.a_y = self.acc_g * math.sin(self.theta_ball + math.pi)

        if STAR_PARTICLE:
            self.drag = DRAG_COEFFICIENT * math.pow(math.hypot(self.v_x,self.v_y),1) + 5
            self.v_x += deltaT * self.a_x #- DRAG_COEFFICIENT * self.v_x * self.v_x * self.v_x / abs(self.v_x)
            self.v_y += deltaT * self.a_y #- DRAG_COEFFICIENT * self.v_y * self.v_y * self.v_y / abs(self.v_y)
        else:
            self.v_x += deltaT * self.a_x
            self.v_y += deltaT * self.a_y
        self.x += deltaT * self.v_x
        self.y += deltaT * self.v_y

        if BOUNDS:
            if self.x >= screenwidth - self.radius - ball.x_padding:
                self.x = screenwidth - self.radius - ball.x_padding
            elif self.x <= 0 + self.radius + ball.x_padding:
                self.x = 0 + self.radius + ball.x_padding
            if self.y >= screenheight - self.radius - ball.y_padding:
                self.y = screenheight - self.radius - ball.y_padding
            elif self.y <= 0 + self.radius + ball.y_padding:
                self.y <= 0 + self.radius + ball.y_padding


    # Checks for collision with another ball (other ball passed as parameter)
    # Updates both ball velocities if collision condition is actually met
    def collision(self,otherball):
        dx = otherball.x - self.x
        dy = otherball.y - self.y
        dist = math.hypot(dx,dy)

        # Checks if the ball areas are overlapping
        if dist <= self.radius + otherball.radius:
            d_vx = otherball.v_x - self.v_x
            d_vy = otherball.v_y - self.v_y

            # Change in ball center distances / time
            # If balls are converging, then collide
            dD_dt = (dx * d_vx + dy * d_vy) / dist
            if dD_dt < 0:
                col_ang = math.atan2(dy,dx)
                tang_ang = col_ang - (math.pi / 2)
                x_ave = (otherball.x + self.x) / 2
                y_ave = (otherball.y + self.y) / 2

                speedself = math.hypot(self.v_x,self.v_y)
                speedother = math.hypot(otherball.v_x,otherball.v_y)

                theta_self = math.atan2(self.v_y,self.v_x)
                theta_other = math.atan2(otherball.v_y,otherball.v_x)

                # DEBUGGING
                # print("BEFORE")
                # print("self.v_x before:", self.v_x)
                # print("other.v_x before:", otherball.v_x)
                # print("self.v_y before:", self.v_y)
                # print("other.v_y before:", otherball.v_y)
                # print("tang_ang:", tang_ang)
                # print("col_ang:",col_ang)
                # print("theta1self before: ", theta_self)
                # print("theta1other: before",theta_other)

                v1c = speedself * math.sin(theta_self - tang_ang)
                v2c = speedother * math.sin(theta_other - tang_ang)

                v1t = speedself * math.cos(theta_self - tang_ang)
                v2t = speedother * math.cos(theta_other - tang_ang)

                # DEBUGGING
                # print("v1c:",v1c)
                # print("v2c:",v2c)
                # print("v1t:", v1t)
                # print("v2t:", v2t)

                # After collision:
                # Using conservation of translational momentum and translational energy
                (v1c,v2c) = ((v1c * (self.mass -  otherball.mass) + 2 * v2c * otherball.mass * ball.elasticity) / (self.mass + otherball.mass), (v2c * (otherball.mass - self.mass) + 2 * v1c * self.mass * ball.elasticity) / (self.mass + otherball.mass))

                # Legacy Collision swap (no accounting for mass differences)
                # (v1c,v2c) = (v2c,v1c)

                self.v_x = v1t * math.cos(tang_ang) - v1c * math.sin(tang_ang)
                self.v_y = v1t * math.sin(tang_ang) + v1c * math.cos(tang_ang)
                # self.v_x = v1c * math.cos(col_ang) - v1t * math.cos(tang_ang)
                # self.v_y = v1c * math.sin(col_ang) - v1t * math.sin(tang_ang)

                otherball.v_x = v2t * math.cos(tang_ang) - v2c * math.sin(tang_ang)
                otherball.v_y = v2t * math.sin(tang_ang) + v2c * math.cos(tang_ang)



                # DEBUGGING
                theta_self = math.atan2(self.v_y,self.v_x)
                theta_other = math.atan2(otherball.v_y,otherball.v_x)
                v1c = speedself * math.sin(theta_self - tang_ang)
                v2c = speedother * math.sin(theta_other - tang_ang)
                v1t = speedself * math.cos(theta_self - tang_ang)
                v2t = speedother * math.cos(theta_other - tang_ang)

                # print("\nAFTER")
                # print("self.v_x after:", self.v_x)
                # print("other.v_x after:", otherball.v_x)
                # print("self.v_y after:", self.v_y)
                # print("other.v_y after:", otherball.v_y)
                # print("theta1self after: ", theta_self)
                # print("theta1other: after",theta_other)
                # print("speedself:",speedself)
                # print("speedother:",speedother)
                # print("v1c:",v1c)
                # print("v2c:",v2c)
                # print("v1t:", v1t)
                # print("v2t:", v2t)
                # print('\n\n')

    # Updates the ball circle to the screen about to be printed
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x),int(self.y)), int(self.radius))



# Game Sequence
class Control(object):
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None,24)

    def startScreen(self):
        done = False
        display_startscreen = True

        #KEYS
        startscreen = 1
        CTRL = False

        #screen event loop
        while done == False and display_startscreen:
            for event in pygame.event.get():

                # Clicking X exit functionality
                if event.type == pygame.QUIT:
                    done = True

                # Exit start screen and enter game
                if event.type == pygame.MOUSEBUTTONDOWN:
                    startscreen += 1
                if startscreen == 2:
                    display_startscreen = False

                # CMD-W exit functionality
                if event.type == pygame.KEYDOWN:
                    # print(pygame.key.name(event.key))
                    if event.key == pygame.K_LMETA or event.key == pygame.K_RMETA:
                        CTRL = True
                    if event.key == pygame.K_w and CTRL == True:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LMETA or event.key == pygame.K_RMETA:
                        CTRL = False

            #Draw image and text
            screen.fill(BLACK)
            if startscreen == 1:
                text = self.font.render("Click to start.", True, (255,255,255))
                screen.blit(text, (screenwidth / 2, screenheight / 2))
            self.clock.tick(90)
            pygame.display.update()


    # Actual Simulation
    def game(self):
        balls = []

        # Generates all balls and initializes them
        for i in range(BALLQUANTITY):
            if STAR_PARTICLE:
                balls.append(ball(random.uniform(screenwidth * (0.4  - (INITALBALLSPREAD / 200)),screenwidth * (0.4 + (INITALBALLSPREAD / 200))),random.uniform(screenheight * (0.5 - (INITALBALLSPREAD / 200)),screenheight * (0.5 + (INITALBALLSPREAD / 200))),random.uniform(BALLMINRADIUS,BALLMAXRADIUS)))
            else:
                balls.append(ball(random.uniform(0,screenwidth),random.uniform(0,screenheight),random.uniform(BALLMINRADIUS,BALLMAXRADIUS)))

        # Delta time implementation
        # For the same experience on different machines (fast or slow frame rates)
        dt = 1

        # For exiting the game loop
        done = False

        # Keys pressed
        CTRL = False

        # Event loop
        while done == False:
            for event in pygame.event.get():

                # Clicking X on the window (exit functionality)
                if event.type == pygame.QUIT:
                    done = True

                # CMD-W (exit functionality)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LMETA or event.key == pygame.K_RMETA:
                        CTRL = True
                    if event.key == pygame.K_w and CTRL == True:
                        done = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LMETA or event.key == pygame.K_RMETA:
                        CTRL = False

            # Background
            screen.fill(BLACK)

            # Collision checking
            for i in range(BALLQUANTITY):
                balls[i].move(dt)
                if PARTICLE_COLLISIONS:
                    for otherball in balls[i+1:]:
                        balls[i].collision(otherball)
                        # checkcounter += 1


            if not STAR_PARTICLE:
                for i in range(BALLQUANTITY):
                    balls[i].draw()

            # Prints balls traveling in the negative x-direction first
            # For pseudo 3D effect
            else:
                sorted_particles = sorted(balls, key=lambda ball: ball.v_x)
                i = 0
                for x in range(BALLQUANTITY):
                    i = x
                    if sorted_particles[i].v_x < 0:
                        sorted_particles[i].draw()
                    else:
                        break

                # Draw Star Particle
                pygame.draw.circle(screen, (94,255,238), (int(G_CENTER_X),int(G_CENTER_Y)), 50)

                # Draw the particles traveling in the positive x-direction last
                for x in range(BALLQUANTITY - i):
                    sorted_particles[i].draw()
                    i += 1

            # Update dt for Delta Time
            dt = self.clock.tick(60)
            pygame.display.update()




# Runs entire sequence of game
def main():
    pygame.init()
    pygame.display.set_mode((screenwidth,screenheight))
    pygame.display.set_caption("Pygame Ball Physics")
    proc = Control()
    proc.startScreen()
    proc.game()
    pygame.quit()
    sys.exit()



# Runs main() if the this file is being run directly (not imported to another program)
if __name__ == "__main__":
    main()

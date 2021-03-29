import pygame
from math import sin,cos,sqrt,pi,atan2,degrees
from random import randint, uniform
import time
import numpy as np

# HELPERS / SETTINGS

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

width, height = 600, 600
counter = 0
frameRate = 200
pygame.init()
screen = pygame.display.set_mode([width,height])

def capture(display,name,pos,size): # (pygame Surface, String, tuple, tuple)
    image = pygame.Surface(size)  # Create image surface
    image.blit(display,(0,0),(pos,size))  # Blit portion of the display to the image
    pygame.image.save(image,name)  # Save the image to the disk

def to_polar(vector):
    x, y = vector[0], vector[1]
    angle = atan2(y,x)
    length = sqrt(x ** 2 + y ** 2)
    return [length, angle]

def to_cartesian(polar_vector):
    radius, angle = polar_vector[0], polar_vector[1]
    return [radius*cos(angle), radius*sin(angle)]

def distance(obj1,obj2):
    return sqrt((obj1.x-obj2.x)**2+(obj1.y-obj2.y)**2)

def drawText(msg, color, x, y, s, center=True):
    screen_text = pygame.font.SysFont("Calibri", s).render(msg, True, color)
    if center:
        rect = screen_text.get_rect()
        rect.center = (int(x), int(y))
    else:
        rect = (int(x), int(y))
    screen.blit(screen_text, rect)

def drawShips(lives,size):
    """For lives, under Score"""
    size *= 0.5
    vertices = [(0,-1*size), (-0.25*size, -0.25*size), (0.25*size, -0.25*size)]
    for i in range(lives):
        screen_vertices = [(40+i*0.65*size+v[0],70+v[1]) for v in vertices]
        pygame.draw.lines(screen, GREEN, True, screen_vertices, 2)


class Ship(object):
    def __init__(self,size):
        self.size = size
        self.rotation_angle = 0
        self.x,self.y = width/2,height/2
        self.velocity = [0,0]
        self.maxspeed = 1
        vertices = [(0.5,0),(-0.25,-0.25),(-0.25,0.25)]
        self.points = [to_polar(v) for v in vertices]
        self.points = [[self.size*r,theta] for [r,theta] in self.points]
        self.color = GREEN
        self.lives = 3
        self.alive = True
        self.reward = 0
        self.distances = np.zeros(8)

    def check_asteroids(self,x,y,asteroids):
        for a in asteroids:
            dist=((a.x - x)**2+(a.y - y)**2)**0.5
            if dist < a.size:
                #print("distance:",dist)
                return ((self.x - x)**2+(self.y - y)**2)**0.5 #.astype(np.float32)

    def measure(self,asteroids):
        """Draw lines radiating outward to measure distances to objects"""

        for i in range(8): #8 directions
            #print(f"Checking direction {i}")
            self.distances[i] = 1
            dist = 0    #start at 0
            #determine angle of this line
            ang = self.rotation_angle + 2*pi*i/8
            c,s = cos(ang),sin(ang)
            #add a small distance and check if that position
            #intersects any asteroids
            while dist < 500:
                dist += 1
                x,y = self.x + dist*c, self.y + dist*s
                intersect = self.check_asteroids(x,y,asteroids)

                if intersect:
                    #print("intersect:", intersect)
                    #dpoints are the distance to the intersection
                    self.distances[i] = intersect/500
                    #print("intersect")
                    break

    def update(self,asteroids):
        self.rotation_angle %= 2*pi
        self.x = self.x + self.velocity[0]#*cos(self.rotation_angle)
        self.y = self.y + self.velocity[1]#*sin(self.rotation_angle)

        if self.x < 0: self.x = width
        if self.x > width: self.x = 0
        if self.y < 0: self.y = height
        if self.y > height:
            self.y = 0

        for a in asteroids:
            if distance(self,a) < 1.25*a.size:
                #self.lives -= 1
                self.alive = False#done = True

                #time.sleep(2)
                #asteroids = [Asteroid() for _ in range(asteroid_count)]

    def draw(self):
        # rotate vertices,convert to x-y format
        self.screen_points = [to_cartesian([r, theta + self.rotation_angle]) for \
                              [r, theta] in self.points]
        self.screen_points = [[self.x + pt[0], self.y + pt[1]] for pt in \
                              self.screen_points]

        pygame.draw.lines(screen, self.color, True, self.screen_points, 2)
        for i, pt in enumerate(self.distances):
            #print("Pt:",pt)
            pygame.draw.line(screen, BLUE, (int(self.x + pt * 300*cos(self.rotation_angle + i * pi / 4)),
                                            int(self.y + pt * 300*sin(self.rotation_angle + i * pi / 4))),
                                            (int(self.x), int(self.y)), 2)
        pygame.draw.line(screen, RED, (int(self.x + 300 * cos(self.rotation_angle)),
                                        int(self.y + 300 * sin(self.rotation_angle))),
                                        (int(self.x), int(self.y)), 2)

class Asteroid():
    def __init__(self,size = 50):
        self.x,self.y = randint(0,width),randint(0,height)
        #Asteroids can't start out too close to ship
        while (200 < self.x < 400) or (200 < self.y < 400):
            self.x, self.y = randint(0, width), randint(0, height)
        self.size = size
        self.velocity = 1
        self.level = 1
        self.sides = randint(6,9)
        self.heading = uniform(0.0,2*pi)
        self.points = [to_cartesian((uniform(0.5*self.size,
                                     1.0*self.size),
                                     2*pi*i/self.sides))
                       for i in range(self.sides)]


        self.screen_points = [[self.x + pt[0],
                               self.y + pt[1]]
                              for pt in self.points]

    def move(self):
        self.x += self.velocity*cos(self.heading)
        self.y += self.velocity*sin(self.heading)
        #wrap
        if self.y < 0:
            self.y = height
        if self.x < 0:
            self.x = width
        if self.y > height:
            self.y = 0
        if self.x > width:
            self.x = 0
        self.screen_points = [[int(self.x + pt[0]), int(self.y + \
                            pt[1])] for pt in self.points]

    def check_bullets(self,asteroids,ship,bullets):
        increase_score = 0
        for b in bullets:
            if distance(self,b) < self.size:
                ship.reward = 10
                if self.level == 1:
                    increase_score += 20
                elif self.level == 2:
                    increase_score += 50
                elif self.level == 3:
                    increase_score += 100
                try:
                    asteroids.remove(self)
                except ValueError:
                    pass
                bullets.remove(b)
                self.level += 1
                if self.level in [2,3]:
                    for i in range(2):
                        new_a = Asteroid(self.size/2)
                        new_a.x,new_a.y = self.x,self.y
                        new_a.level = self.level
                        asteroids.append(new_a)
        return increase_score

    def draw(self):
        pygame.draw.lines(screen, GREEN, True, self.screen_points, 2)

class Bullet():
    def __init__(self, x, y, heading):
        self.x = x
        self.y = y
        self.heading = heading
        self.speed = 10
        self.life = 50

    def update(self):
        # update location
        self.x += self.speed * cos(self.heading)
        self.y += self.speed * sin(self.heading)
        # wrap around screen
        if self.x > width:
            self.x = 0
        elif self.x < 0:
            self.x = width
        elif self.y > height:
            self.y = 0
        elif self.y < 0:
            self.y = height
        self.life -= 1
        pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), 3)

pygame.display.set_caption("Pygame Template")
clock = pygame.time.Clock()

class Game(object):
    global asteroids,bullets

    def __init__(self):
        self.done=False

        self.ship = Ship(50)
        self.score = 0
        self.bullets = []
        self.create_bullet = True
        self.asteroid_count = 4
        self.asteroids = [Asteroid() for _ in range(self.asteroid_count)]

    def reset(self):
        self.__init__()
        return self.ship.distances

    def play_frame(self,action):
        global counter
        self.done = False

        counter += 1
        #while not done:
        #Update the game state with action from NN
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if pygame window is closed by user
                self.done = True
        if action == 0:
            self.ship.rotation_angle -= 0.05
        if action == 1:
            self.ship.rotation_angle += 0.05
        if action == 2:
            if len(self.bullets) < 3 and self.create_bullet:
                self.bullets.append(Bullet(self.ship.x, self.ship.y,
                                           self.ship.rotation_angle))
                self.createBullet = False
                bullet_wait = time.time()
        if action == 3:
            self.ship.velocity[0] += cos(self.ship.rotation_angle)
            if self.ship.velocity[0] > self.ship.maxspeed:
                self.ship.velocity[0] = self.ship.maxspeed
            if self.ship.velocity[0] < -self.ship.maxspeed:
                self.ship.velocity[0] = -self.ship.maxspeed

            self.ship.velocity[1] += sin(self.ship.rotation_angle)
            if self.ship.velocity[1] > self.ship.maxspeed:
                self.ship.velocity[1] = self.ship.maxspeed
            if self.ship.velocity[1] < -self.ship.maxspeed:
                self.ship.velocity[1] = -self.ship.maxspeed

        #Draw the scene
        screen.fill(BLACK)
        self.ship.reward = 0
        self.ship.measure(self.asteroids)
        self.ship.update(self.asteroids)
        state = np.array(self.ship.distances,dtype=np.float32)

        self.ship.draw()
        if not self.ship.alive:
            self.ship.reward = -10
            # drawText("GAME OVER", RED, width / 2, 200, 36, True)
            # pygame.display.update()
            # time.sleep(5)
            #pygame.quit()
            self.done = True

        if len(self.asteroids) == 0:
            time.sleep(1)
            self.asteroid_count += 2
            self.asteroids = [Asteroid() for i in range(self.asteroid_count)]

        for a in self.asteroids:
            a.move()
            self.score += a.check_bullets(self.asteroids,self.ship,self.bullets)
            a.draw()

        if self.create_bullet == False and time.time() - bullet_wait >= 0.3:
            self.create_bullet = True
        for b in self.bullets:
            b.update()
            if b.life <= 0:
                try:
                    self.bullets.remove(b)
                except:
                    pass
        # Draw score
        drawText("Score: " + str(self.score), GREEN, 20, 20, 24, False)
        # Draw ships for lives
        #drawShips(ship.lives, ship.size)

        pygame.display.flip()
        #clock.tick(frameRate)
        # for saving screenshots
        #if counter %5 == 0:
        #capture(screen, 'Asteroids{}.png'.format(counter), (0, 0), (600, 600))

        return state,self.ship.reward,self.done,self.score


    #pygame.quit()

if __name__ == "__main__":
    g = Game()
    for i in range(100):
        g.play_frame(2)
        g.ship.measure(g.asteroids)
        print("distances",g.ship.distances)

"""
March 23, 2021 After 1 hour of training with graphics:
***Episode 440 *** \                      
Av.steps: [last 10]: 140.70,[last 100]: 207.67, [all]: 327.27                         
epsilon: 0.01, frames_total: 144324, score: 80
Elapsed time: 01:07:38

***Episode 450 *** \                      
Av.steps: [last 10]: 212.00,[last 100]: 218.09, [all]: 324.71                         
epsilon: 0.01, frames_total: 146444, score: 3600
Elapsed time: 01:08:41

***Episode 460 *** \                      
Av.steps: [last 10]: 326.90,[last 100]: 242.20, [all]: 324.76                         
epsilon: 0.01, frames_total: 149713, score: 280
Elapsed time: 01:10:27

***Episode 470 *** \                      
Av.steps: [last 10]: 157.30,[last 100]: 233.30, [all]: 321.20                         
epsilon: 0.01, frames_total: 151286, score: 890
Elapsed time: 01:11:23

***Episode 100 *** \                      
Av.scores: [last 10]: 1660.00,[last 100]: 1263.60, [all]: 2228.59                         
epsilon: 0.01, frames_total: 64094, last score: 1660, high score: 7560
Elapsed time: 00:25:26

***Episode 300 *** \                      
Av.scores: [last 10]: 2584.00,[last 100]: 2614.60, [all]: 2915.84                         
epsilon: 0.01, frames_total: 158028, last score: 20, high score: 9830
Elapsed time: 01:04:23

"""
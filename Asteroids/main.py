import pygame
import vectors
import time
from random import randint, uniform
from math import pi, sqrt, cos, sin, atan2
from linear_solver import do_segments_intersect
# drawing measurement lines
# define constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
VIOLET = (148, 0, 211)

width,height = 600,600
asteroid_count = 10
score = 0

def length(v):
    return sqrt(sum([coord ** 2 for coord in v]))

def distance(obj1,obj2):
    return sqrt((obj1.x-obj2.x)**2+(obj1.y-obj2.y)**2)

def distance_pts(x1,y1,x2,y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def to_cartesian(polar_vector):
    radius, angle = polar_vector[0], polar_vector[1]
    return [radius*cos(angle), radius*sin(angle)]

def to_polar(vector):
    x, y = vector[0], vector[1]
    angle = atan2(y,x)
    return [length(vector), angle]

# Create function to draw texts
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
        screen_vertices = [(int(40+i*0.65*size+v[0]),int(70+v[1])) for v in vertices]
        pygame.draw.lines(screen, GREEN, True, screen_vertices, 2)

class PolygonModel():
    def __init__(self,points):
        self.points = points
        self.rotation_angle = 0
        self.x = 0
        self.y = 0

class Ship(PolygonModel):
    def __init__(self,size):
        self.size = size
        self.rotation_angle = 0
        self.x, self.y = width / 2, height / 2
        vertices = [(0.5,0),(-0.25,-0.25),(-0.25,0.25)]
        #convert x-y vertices to polar
        self.points = [to_polar(v) for v in vertices]
        #scale up ship by self.size
        self.points = [[self.size*r,theta] for [r,theta] in self.points]
        self.color = GREEN
        self.lives = 3
        self.dpoints = [] #points for testing distance measurements

    def update(self):
        global asteroids
        for a in asteroids:
            if distance(self,a) < a.size:
                self.lives -= 1
                time.sleep(2)
                asteroids = [Asteroid() for _ in range(asteroid_count)]

    def draw(self):
        #rotate vertices,convert to x-y format
        cartesian_points = [to_cartesian([r,theta+self.rotation_angle]) for [r,theta] in self.points]
        self.screen_points = [[int(self.x + pt[0]),int(self.y+pt[1])] for pt in cartesian_points]

        pygame.draw.lines(screen, self.color, True, self.screen_points, 2)

    def check_asteroids(self,x,y):
        for a in asteroids:
            if distance_pts(x, y, a.x, a.y) < a.size:

                return x,y

    def measure(self):
        """Draw lines radiating outward to measure distances to objects"""

        self.dpoints = []
        for i in range(8):
            dist = 0
            while dist < 500:
                dist += 1
                x,y = ship.x + dist*cos(self.rotation_angle + 2*pi*i/8),\
                      ship.y + dist*sin(self.rotation_angle + 2*pi*i/8)
                intersect = self.check_asteroids(x,y)
                if intersect:
                    self.dpoints.append(intersect)
                    break

        #return self.dpoints #x,y #dist
class Asteroid():
    def __init__(self,size = 50):
        self.x,self.y = randint(0,width),randint(0,height)
        self.size = size
        self.level = 1
        self.sides = randint(6,9)
        self.heading = uniform(0.0,2*pi)
        self.points = [to_cartesian((uniform(0.5*self.size,
                                             1.0*self.size),
                                     2*pi*i/self.sides)) \
                       for i in range(self.sides)]
        self.screen_points = [[self.x + pt[0],
                               self.y+pt[1]]
                              for pt in self.points]

    def move(self):
        self.x += 0.5*cos(self.heading)
        self.y += 0.5*sin(self.heading)
        #wrap
        if self.y < 0:
            self.y = height
        if self.x < 0:
            self.x = width
        if self.y > height:
            self.y = 0
        if self.x > width:
            self.x = 0

        self.screen_points = [[int(self.x + pt[0]), int(self.y + pt[1])] for pt in self.points]

    def check_bullets(self):
        global score
        for b in bullets:
            if distance(self,b) < self.size:
                if self.level == 1:
                    score += 20
                elif self.level == 2:
                    score += 50
                elif self.level == 3:
                    score += 100
                asteroids.remove(self)
                bullets.remove(b)
                self.level += 1
                if self.level in [2,3]:
                    for i in range(2):
                        new_a = Asteroid(self.size/2)
                        new_a.x,new_a.y = self.x,self.y
                        new_a.level = self.level
                        asteroids.append(new_a)


    def draw(self):
        pygame.draw.lines(screen, GREEN, True, self.screen_points, 2)

class Bullet():
    def __init__(self, x, y, heading):
        self.x = x
        self.y = y
        self.heading = heading
        self.speed = 10
        self.life = 30

    def update(self):
        # Moving
        self.x += self.speed * cos(self.heading)
        self.y += self.speed * sin(self.heading)

        pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), 3)

        if self.x > width:
            self.x = 0
        elif self.x < 0:
            self.x = width
        elif self.y > height:
            self.y = 0
        elif self.y < 0:
            self.y = height
        self.life -= 1

createBullet = True
# set up display
pygame.init()
screen = pygame.display.set_mode([width, height])

#in case you use fonts:
pygame.font.init()
myfont = pygame.font.SysFont('Consolas', 24)
scorefont = pygame.font.SysFont('Consolas', 72)

pygame.display.set_caption('Pygame Window') #add your own caption!
FPS = 60  # frames per second
clock = pygame.time.Clock()

counter = 0 #frame count

# loop until user clicks the close button
done = False

#Rendering the Game

ship = Ship(50)
bullets = []

asteroids = [Asteroid() for _ in range(asteroid_count)]

# for ast in asteroids:
#     ast.x = randint(0,width)
#     ast.y = randint(0,height)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # if pygame window is closed by user
            done = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship.rotation_angle -= 0.1
    if keys[pygame.K_RIGHT]:
        ship.rotation_angle += 0.1
    if keys[pygame.K_SPACE]:
        if len(bullets) < 4 and createBullet:
            bullets.append(Bullet(ship.x,ship.y,ship.rotation_angle))
            createBullet = False
            bullet_wait = time.time()
    if keys[pygame.K_p]:
        if FPS == 60:
            FPS = 300  #faster display
        else:
            FPS = 60
    # fill the screen with background color
    screen.fill(BLACK)

    counter += 1
    ship.update()
    ship.measure()
    #print(len(ship.dpoints))
    for pt in ship.dpoints:
        pygame.draw.line(screen,BLUE,(int(pt[0]),int(pt[1])), (int(ship.x), int(ship.y)),2)

    #x,y = ship.measure() #d*cos(ship.rotation_angle), d*sin(ship.rotation_angle)
    #pygame.draw.line(screen, RED, (int(x), int(y)))
    #drawText("d: "+str(d), RED, 120, 120, 24, False)
    #drawText("d: " + str(ship.rotation_angle), RED, 120, 150, 24, False)
    ship.draw()

    if ship.lives == 0:
        drawText("GAME OVER",GREEN,width/2,200,36,True)
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
    if len(asteroids) == 0:
        time.sleep(2)
        asteroid_count += 2
        asteroids = [Asteroid() for i in range(asteroid_count)]
    for a in asteroids:
        a.move()
        a.check_bullets()
        a.draw()

    if createBullet == False and time.time() - bullet_wait >= 0.2:
        createBullet = True
    for b in bullets:
        b.update()
        if b.life <= 0:
            try:
                bullets.remove(b)
            except:
                pass

    # Draw score
    drawText("Score: "+str(score), GREEN, 20, 20, 24, False)
    # Draw ships for lives
    drawShips(ship.lives,ship.size)

    pygame.display.update()

    # for saving screenshots:
    # if counter %5 == 0:
    # Capture(screen, 'Capture{}.png'.format(counter), (0, 0), (600, 600))
    clock.tick(FPS)
pygame.quit()

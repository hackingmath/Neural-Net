import pygame
import time
from math import pi, sqrt, cos, sin, atan2
import neuralNetwork as nn
import polar_cartesian as pc
import numpy
from asteroid import Asteroid
from bullet import Bullet

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
GRAPHICS_ON = True
AI_PLAYING = True

# Create function to draw texts
def drawText(msg, color, x, y, s, center=True):
    screen_text = pygame.font.SysFont("Calibri", s).render(msg, True, color)
    if center:
        rect = screen_text.get_rect()
        rect.center = (int(x), int(y))
    else:
        rect = (int(x), int(y))
    screen.blit(screen_text, rect)

class Ship():
    def __init__(self,size=50,width=600,height=600,graphics=True,brain=None):
        self.size = size
        self.rotation_angle = 0
        self.x, self.y = width / 2, height / 2
        vertices = [(0.5,0),(-0.25,-0.25),(-0.25,0.25)]
        #convert x-y vertices to polar
        self.points = [pc.to_polar(v) for v in vertices]
        #scale up ship by self.size
        self.points = [[self.size*r,theta] for [r,theta] in self.points]
        self.color = GREEN
        self.score = 0 #game score
        self.alive = True
        self.life = 0 #number of frames survived
        self.dpoints = [0] * 8 #points for testing distance measurements
        self.create_asteroids = False
        self.shoot_bullet = False #True when key pressed or AI chooses
        self.createBullet = True #Off when bullet has been created, creates delay
        self.bullet_wait = 0
        self.graphics = graphics
        self.fitness = 0
        #for neural net
        if brain:
            self.brain = brain.replicate()
        else:
            self.brain = nn.NeuralNetwork(8, 12, 3, 0.3)
        self.inputs = [0] * 5
        self.output = numpy.zeros(3)

    def update(self,asteroids,asteroid_count):
        self.life += 1
        for a in asteroids:
            if pc.distance(self,a) < a.size:
                self.alive = False
                return
        #if shooting, wait before creating another bullet
        if self.createBullet == False and time.time() - self.bullet_wait >= 0.2:
            self.createBullet = True

    def draw(self):
        #rotate vertices,convert to x-y format
        cartesian_points = [pc.to_cartesian([r,theta+self.rotation_angle]) for [r,theta] in self.points]
        self.screen_points = [[int(self.x + pt[0]),int(self.y+pt[1])] for pt in cartesian_points]

    def get_score(self):
        return self.score

    def check_asteroids(self,x,y,asteroids):
        for a in asteroids:
            if pc.distance_pts(x, y, a.x, a.y) < a.size:

                return x,y

    def measure(self,asteroids):
        """Draw lines radiating outward to measure distances to objects"""


        for i in range(8):
            dist = 0
            ang = self.rotation_angle + 2*pi*i/8
            c,s = cos(ang),sin(ang)
            while dist < 500:
                dist += 1
                x,y = self.x + dist*c, self.y + dist*s
                intersect = self.check_asteroids(x,y,asteroids)
                if intersect:
                    self.dpoints[i] = intersect
                    #print("intersect")
                    break

    def left(self):
        """AI turns left"""
        self.rotation_angle -= 0.1
        #print("Left")

    def right(self):
        """AI turns right"""
        self.rotation_angle += 0.1
        #print("Right")

    def shoot(self,bulletList):
        """AI shoots bullet"""
        #print("Shoot")
        self.shoot_bullet = True

    def think(self,bulletList):
        #
        self.inputs = numpy.zeros(8)
        for j,pt in enumerate(self.dpoints):
            if pt != 0:
                self.inputs[j] = pc.sq_dist(self,pt)
        self.output = self.brain.query(numpy.array(self.inputs))  #
        if numpy.argmax(self.output) == 0:  # left
            self.left()
        elif numpy.argmax(self.output) == 1:  # right
            self.right()
        elif numpy.argmax(self.output) == 2:
            self.shoot(bulletList)

    def calcFitness(self,ships):
        #total = sum([ship.get_score() for ship in ships])
        self.fitness = self.get_score() + self.life# / total

    def play(self):
        global asteroid_count
        pygame.init()

        if GRAPHICS_ON:
            # set up display

            screen = pygame.display.set_mode([width, height])

            #in case you use fonts:
            pygame.font.init()
            myfont = pygame.font.SysFont('Consolas', 24)
            scorefont = pygame.font.SysFont('Consolas', 72)

            pygame.display.set_caption('Pygame Window') #add your own caption!

        FPS = 300  # frames per second
        clock = pygame.time.Clock()

        counter = 0 #frame count

        # loop until user clicks the close button
        done = False

        #create the objects
        # ship = Ship(50,width,height,True)
        bullets = []
        asteroids = [Asteroid() for _ in range(asteroid_count)]

        while self.alive and not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if pygame window is closed by user
                    done = True
            if not AI_PLAYING:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.rotation_angle -= 0.1
                if keys[pygame.K_RIGHT]:
                    self.rotation_angle += 0.1
                if keys[pygame.K_SPACE]:
                    self.shoot(bullets)

                if keys[pygame.K_p]:
                    if FPS == 60:
                        FPS = 300  #faster display
                    else:
                        FPS = 60
            if GRAPHICS_ON:
                # fill the screen with background color
                screen.fill(BLACK)

            counter += 1
            if AI_PLAYING:
                self.think(bullets)

            self.update(asteroids,asteroid_count)
            if len(bullets) < 4 and self.createBullet and self.shoot_bullet:
                bullets.append(Bullet(self.x, self.y, self.rotation_angle,GRAPHICS_ON))
                self.shoot_bullet = False
                self.createBullet = False
                self.bullet_wait = time.time()
            self.measure(asteroids)
            if self.create_asteroids:
                asteroids = [Asteroid() for _ in range(asteroid_count)]
            if GRAPHICS_ON:
                for pt in self.dpoints:
                    if pt != 0:
                        pygame.draw.line(screen,BLUE,(int(pt[0]),int(pt[1])), (int(self.x), int(self.y)),2)

            #draw ship:
            if GRAPHICS_ON:
                self.draw()
                pygame.draw.lines(screen, self.color, True, self.screen_points, 2)

            if len(asteroids) == 0:
                time.sleep(2)
                asteroid_count += 2
                asteroids = [Asteroid() for i in range(asteroid_count)]
            for a in asteroids:
                a.move()
                a.check_bullets(self,asteroids,bullets)
                if GRAPHICS_ON:
                    #draw asteroids
                    pygame.draw.lines(screen, GREEN, True, a.screen_points, 2)
                    #a.draw()

            for b in bullets:
                b.update()
                if GRAPHICS_ON:
                    pygame.draw.circle(screen, GREEN, (int(b.x), int(b.y)), 3)
                if b.life <= 0:
                    try:
                        bullets.remove(b)
                    except:
                        pass



            #print()
            # for saving screenshots:
            # if counter %5 == 0:
            # Capture(screen, 'Capture{}.png'.format(counter), (0, 0), (600, 600))
            clock.tick(FPS)
            if GRAPHICS_ON:
                pygame.display.update()
        pygame.quit()
        return self.score + self.life

s = Ship(50,600,600,True)
s.play()
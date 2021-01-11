# AI for Asteroids

This is the code to a Live Project for Manning Publications, a tutorial on how to create a working clone of the Asteroids video game and to code an AI to play it.

## Description

The code is in Python, using Pygame as the graphics library and numpy for the matrix calculations in the Neural Network. The polar_cartesian file is helper code from Paul Orland's Math for Programmers, the book this Live Project is officially based on.

## Getting Started

### Dependencies

* Intall Python 3
* Install Pycharm - highly recommended because it automatically creates a virtual environment for all the dependencies you install for your project.
* Install Pygame and Numpy.

### Installing

* Put the files from the "November2020" directory in a Pycharm project.

### Executing program

* Put all the files into a project, on Pycharm for example.

* To play manually, run ship_ai_m5.py with these settings
```
GRAPHICS_ON = True
AI_PLAYING = False
```
* To have the AI play, and to watch the game, run ga_m5.py with these settings at the beginning of ship_ai_PF:
```
GRAPHICS_ON = True
AI_PLAYING = True
```

* To have the AI play, and to disable the graphics, run ga.py with these settings at the beginning of ship_ai_m5:
```
GRAPHICS_ON = False
AI_PLAYING = True
```

* The plan is to have the program play hundreds of ships at a time or one after the other very quickly, but as of now it runs rather slowly. Any constructive input is welcome!

## Help

I'm asking for *your* help to test and debug this code! Let me know if you have improvements. peter@techymath.com

## Authors

Peter Farrell aka Techy Math  
[@hackingmath](https://twitter.com/hackingmath)


## Acknowledgments

Last year I was inspired by Dan Shiffman to make an AI play Flappy Bird like he did, and the YouTuber CodeBullet inspired me to tackle Asteroids. The only difference is their programs worked! The Neural Network is closely based on the DIY net in the excellent book Make Your Own Neural Network by Tariq Rashid.

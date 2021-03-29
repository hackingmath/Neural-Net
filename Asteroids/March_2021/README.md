# Creating an AI to play Asteroids
I created a pygame version of Asteroids, then attempted to use Deep Q Learning to train it. It flies around
admirably and gets and average of a few thousand points but doesn't seem to master it.</br>
I trained it for 36 hours and its high score was 17,000 points but the average of those 5000 games was a tenth of that.</br>
Install Pytorch and Matplotlib, and Pygame if you're going to use the graphics.</br>
Put game_move.py and dueling_DQN.py in the same directory and run dueling_DQN.py. You'll be 
able to see the ship moving, turning and shooting. Every 10 games it'll print out the 
average scores and at the end of 200 games it'll display a graph of the running average
of the scores of 100 games.</br>

Can you help me optimize it? Please email me at peterfarrell66@gmail.com with comments and suggestions.

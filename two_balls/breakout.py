# See https://www.101computing.net/breakout-tutorial-using-pygame-adding-a-brick-wall/
#Import the pygame library and initialise the game engine
import pygame
#Let's import the Paddle Class & the ball_1 Class
from paddle import Paddle
from ball import Ball
from brick import Brick
import numpy as np
import copy
 
pygame.init()
 
# Define some colors
WHITE = (255,255,255)
DARKBLUE = (36,90,190)
LIGHTBLUE = (0,176,240)
RED = (255,0,0)
ORANGE = (255,100,0)
YELLOW = (255,255,0)
 
score = 0
lives = 3
 
# Open a new window
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout Game")
 
#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()
 
#Create the Paddle
paddle = Paddle(LIGHTBLUE, 100, 10)
paddle.rect.x = 350
paddle.rect.y = 560
 
#Create the ball_1 sprite
speed_ball=2
#ball_1 = Ball(WHITE,10,10)
ball_1 = Ball(WHITE,10,10,speed_ball)
ball_1.rect.x = 345
ball_1.rect.y = 195

ball_2 = Ball(WHITE,10,10,speed_ball)
ball_2.rect.x = 345
ball_2.rect.y = 195
 
all_bricks = pygame.sprite.Group()

#original size: 
#brick_size=[80,30]
brick_size=[8,8]

x_number=int(np.floor(7*80/(brick_size[0]*1.3)))
x_spacing=int(np.floor(100/(80/(brick_size[0]*1.3))))

y_number=int(np.floor(40/(brick_size[1]*1.3)))
y_spacing=int(np.floor(40/y_number))

for y in range(y_number):
	for i in range(x_number):
		brick = Brick(RED,brick_size[0],brick_size[1])
		brick.rect.x = 60 + i* x_spacing
		brick.rect.y = 60 + y*y_spacing
		all_sprites_list.add(brick)
		all_bricks.add(brick)
	for i in range(x_number):
		brick = Brick(ORANGE,brick_size[0],brick_size[1])
		brick.rect.x = 60 + i* x_spacing
		brick.rect.y = 100 + y*y_spacing
		all_sprites_list.add(brick)
		all_bricks.add(brick)
	for i in range(x_number):
		brick = Brick(YELLOW,brick_size[0],brick_size[1])
		brick.rect.x = 60 + i* x_spacing
		brick.rect.y = 140 + y*y_spacing
		all_sprites_list.add(brick)
		all_bricks.add(brick)
 
# Add the paddle to the list of sprites
all_sprites_list.add(paddle)


all_sprites_list.add(ball_1)
#balls=[ball_1]
all_sprites_list.add(ball_2)
balls=[ball_1,ball_2]


# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True
 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while carryOn:
	# --- Main event loop
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
				carryOn = False # Flag that we are done so we exit this loop
 
	#Moving the paddle when the use uses the arrow keys
	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT]:
		paddle.moveLeft(5)
	if keys[pygame.K_RIGHT]:
		paddle.moveRight(5)
 
	# --- Game logic should go here
	all_sprites_list.update()
	
	for ball in balls:
		#Check if the ball is bouncing against any of the 4 walls:
		if ball.rect.x>=790:
			ball.velocity[0] = -ball.velocity[0]
		if ball.rect.x<=0:
			ball.velocity[0] = -ball.velocity[0]
		if ball.rect.y>590:
			ball.velocity[1] = -ball.velocity[1]
			lives -= 1
			if lives == 0:
				#Display Game Over Message for 3 seconds
				font = pygame.font.Font(None, 74)
				text = font.render("GAME OVER", 1, WHITE)
				screen.blit(text, (250,300))
				pygame.display.flip()
				pygame.time.wait(3000)
	 
				#Stop the Game
				carryOn=False
 
	for ball in balls:
		if ball.rect.y<40:
			ball.velocity[1] = -ball.velocity[1]
 
	#Detect collisions between the ball and the paddles
	for ball in balls:
		if pygame.sprite.collide_mask(ball, paddle):
			ball.rect.x -= ball.velocity[0]
			ball.rect.y -= ball.velocity[1]
			ball.bounce()
 
	#Check if there is the ball collides with any of bricks
	for ball in balls:
		brick_collision_list = pygame.sprite.spritecollide(ball,all_bricks,False)
		for brick in brick_collision_list:
			ball.bounce()
			score += 1
			brick.kill()
			if len(all_bricks)==0:
				#Display Level Complete Message for 3 seconds
				font = pygame.font.Font(None, 74)
				text = font.render("LEVEL COMPLETE", 1, WHITE)
				screen.blit(text, (200,300))
				pygame.display.flip()
				pygame.time.wait(3000)
	 
				#Stop the Game
				carryOn=False
 
	# --- Drawing code should go here
	# First, clear the screen to dark blue.
	screen.fill(DARKBLUE)
	pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 2)
 
	#Display the score and the number of lives at the top of the screen
	font = pygame.font.Font(None, 34)
	text = font.render("Score: " + str(score), 1, WHITE)
	screen.blit(text, (20,10))
	text = font.render("Lives: " + str(lives), 1, WHITE)
	screen.blit(text, (650,10))
 
	#Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
	all_sprites_list.draw(screen)
 
	# --- Go ahead and update the screen with what we've drawn.
	pygame.display.flip()
 
	# --- Limit to 60 frames per second
	clock.tick(60)
 
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()

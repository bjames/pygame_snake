"""
    This python "Snake" clone was designed as a teaching tool for distribution to IDEAL Video Game Design Camp Students
	This program was created in 2 hours on a Saturday by an intermediate programmer and is NOT meant to be a perfect example of programming practices
	I urge any reading this to implement snake themselves, it is a good learning exercise and will be beneficial. Look at some of the ways things
	are implemented in this file and find better ways to implement them
	
    Copyright (C) 2014  Brandon James - bjames1530@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.olrg/licenses/>.
	
"""


import pygame #import the pygame library
import random #import the random library
from collections import deque #from the collections library import deque

#Configuration Variables
WINDOW = [600, 500] #variable for the window size in pixels (X, Y)
BG_COLOR = (255, 255, 255) #Variable for background color in in RBG notation
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
FPS = 30 #variable used to store target frame rate
X_SPEED = 4 #speed in px per cycle of the controlled char
Y_SPEED = X_SPEED #allows you to easily play with different horizontal and vertical speeds

#initialize pygame
pygame.init()
screen = pygame.display.set_mode(WINDOW) #sets display size
pygame.display.set_caption('IDEAL - SNAKE CLONE') #sets display caption
screen.fill(BG_COLOR) #sets display background
clock = pygame.time.Clock()#used to set FPS

#initialize the random number generator
random.seed() #initializes python's built-in psuedorandom generator using system time as the seed


def endGame():

	END_FONT = pygame.font.Font(None, 72) #set up the endGame font, size 72
	END_GAME = END_FONT.render("GAME OVER", 1, (255, 0, 0)) #render the text in red
	END_POS = END_GAME.get_rect() #gets the area of the surface
	END_POS.centerx = screen.get_rect().centerx #gets the center point of the surface
	screen.blit(END_GAME, END_POS) #'blits' the rendered font (writes it to the graphics memory)
	pygame.display.update #refreshes the display (draws a new frame)
	
	pygame.time.delay(500) #makes the user wait for 500ms before going to the main menu
	
def game():

	SCORE_FONT = pygame.font.Font(None, 36)

	#set default values
	snakePos = [WINDOW[0]/2, WINDOW[1]/2] #by default, the snake begins in the middle of the screen
	applePos = [random.randint(10, WINDOW[0] - 10), random.randint(10, WINDOW[1] - 10)] #the apple is placed in a random location a minimum of 10px away from the border
	score = 0 #score is set to zero
	snakeTail = deque() #here we are setting a list called "snakeTail" to be used as a queue structure
	dir = 0 #0 = no movement, 1 = Y+, 2 = Y-, 3 = X+, 4 = X-

	#game loop control
	run = True #run is a boolean variable it can hold two values, True (1) or False (0)

	#game loop
	while run: #this loop will continue until run is False

		clock.tick(30) #set the target FPS, 24 is normally the bare minimum for a screen to look like video instead of a 'fast slideshow'
		
		if not snakePos in snakeTail: #if the current position of the snake is not in the snakeTail list then added it
			snakeTail.append(snakePos[:]) #append the snakePos to snakeTail 
		
		#exits loop when the window is closed
		for event in pygame.event.get():
				if event.type == pygame.QUIT: #close button
						run = False
		
		#returns a list of all the keys currently pressed
		keys = pygame.key.get_pressed()
		
		#get keyboard input, this changes the current direction of the snake
		if keys[pygame.K_a] and not dir == 3: #the snake cannot do a 180 without eating itself
			dir = 4
		if keys[pygame.K_s] and not dir == 1: 
			dir = 2
		if keys[pygame.K_d] and not dir == 4:
			dir = 3
		if keys[pygame.K_w] and not dir == 2: 
			dir = 1
		if keys[pygame.K_SPACE]:
			dir = 0 #here the game is paused until a key is pressed
			
		#move the snake
		if dir == 1:
			snakePos[1] = snakePos[1] - Y_SPEED	 #if dir is 1 move in the Y- direction
		elif dir == 2:
			snakePos[1] = snakePos[1] + Y_SPEED
		elif dir == 3:	
			snakePos[0] = snakePos[0] + X_SPEED
		elif dir == 4:
			snakePos[0] = snakePos[0] - X_SPEED 
		else:
			pass #if the direction is not 1, 2, 3, or 4, do nothing
			
		#the apple has a 9px hit box surrounding it. If the snake comes within 9 px then the apple is eaten
		if abs(snakePos[0] - applePos[0]) < 9 and abs(snakePos[1] - applePos[1]) < 9:
			score = score + 1
			applePos = [random.randint(10, WINDOW[0] - 10), random.randint(10, WINDOW[1] - 10)]

		#the tail length starts at 5 and increases by two each time an apple is eaten	
		while len(snakeTail) >= (score * 2) + 5:
			snakeTail.popleft()
		
		#display score
		screen.fill(BG_COLOR) #clear the screen to prevent ghosting
		text = SCORE_FONT.render(str(score), 1, (10, 10, 10)) #render the score, note that we must cast the variable from an int to a string 
		screen.blit(text, (5, 10)) #move the text to graphics memory
		
		i = 0 #i will be used to iterate through the snake tail list
		
		#draw the snake's tail
		while (i) < len(snakeTail): #loop through the snakeTail list and draw it to screen, please note that this is not an efficient method
			pygame.draw.circle(screen, SNAKE_COLOR, snakeTail[i], 5) #for a small game like this it is fine, but for larger games it might be best
			i = i+1													 #to keep track of pivot points and the head and tail, then draw all the intermediates
		
		#draw the snake's head
		pygame.draw.circle(screen, SNAKE_COLOR, snakePos, 5)
		
		#draw the apple
		pygame.draw.circle(screen, APPLE_COLOR, applePos, 5) 

		#this checks to see if the snake is dead or alive, the snake dies if it leaves the bondry or bites itself
		if snakePos[0] < 0 or snakePos[1] < 0 or snakePos[0] > WINDOW[0] or snakePos[1] > WINDOW[1] or snakePos in snakeTail and dir != 0:
			endGame()
			run = False
		
		pygame.display.update() #refresh the display
		

def main():
	
	#boolean variable for the main menu loop
	run = True

	#loop for the main menu
	while run:
	
		#set the target FPS to 30
		clock.tick(FPS)

		#exits loop when the window is closed
		for event in pygame.event.get():
				if event.type == pygame.QUIT: #close button
						run = False
		
		screen.fill(BG_COLOR) #fill the screen with the background color	
		title = pygame.font.Font(None, 72) #set the title font
		subTitle = pygame.font.Font(None, 36) #set the subtitle font
		subTitle = subTitle.render("SPACE to start, ESC to quit, WASD to move", 1, APPLE_COLOR) #render the subtitle
		title = title.render("SNAKE", 1, SNAKE_COLOR) #render the title
		title_pos = title.get_rect() #get the area of the screen
		title_pos.centerx = screen.get_rect().centerx #get the centerpoint
		screen.blit(subTitle, (40, 300)) #blit the subtitle
		screen.blit(title, title_pos) #blit the title
		
		
		keys = pygame.key.get_pressed() #get the pressed keys
		
		if keys[pygame.K_SPACE]:
		
			game() #call the game function
			
			#once the game function has finished display the game over text
			END_FONT = pygame.font.Font(None, 72)
			END_GAME = END_FONT.render("GAME OVER", 1, (255, 0, 0))
			END_POS = END_GAME.get_rect()
			END_POS.centerx = screen.get_rect().centerx
			screen.blit(END_GAME, END_POS)
			pygame.display.update
	
			pygame.time.delay(3000) #delay for three seconds
			
		elif keys[pygame.K_ESCAPE]: #if escape is pressed then exit
			run = False 
			

		pygame.display.update() #refresh the display


main()
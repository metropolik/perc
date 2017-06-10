#!/usr/bin/python
import pygame, sys
from pygame.locals import *
from time import time
from random import random
import numpy as np
from copy import deepcopy

pygame.init()
fpsClock = pygame.time.Clock()
wwidth = 800
wheight = 600
wso = pygame.display.set_mode((wwidth, 600))
pygame.display.set_caption('Perceptron')

redColor = pygame.Color(255, 0, 0)
blueColor = pygame.Color(0, 0, 255)
whiteColor = pygame.Color(255, 255, 255)
blackColor = pygame.Color(0, 0, 0)
greyColor = pygame.Color(200, 200, 200)
yellowColor = pygame.Color(255, 235, 65)
mx, my = 0, 0
learningRate = 1.0

pointsRed = [(-0.4, 0.8), (-0.8, -0.2)] #-1 #A
pointsBlue = [(0.3, 1.6), (-0.4, 1.5)] #1 #B
placingRed = True
training = False
timeNextStep = 0
w = [0, 1, -1]

transform = np.array([[1.0, 0.0, wwidth/2.0], 
					  [0.0, 1.0, wheight/2.0],
					  [0.0, 0.0, 1.0]])
scalef = 140.0
scale = np.array([[scalef, 0.0, 0.0],
				  [0.0, -scalef, 0.0],
				  [0.0, 0.0, 1.0]])

# apply currently set transformations to a point
# specified by transform matrix and scale matrix
def t(x):
	if (type(x) != np.ndarray 
		and type(x) in [list, tuple]):
		x = np.array(x)
	else:
		raise Exception("neither array nor list " + str(type(x)))		
	x = np.append(x, [1.0])	#add 1 component to make homogeneous
	x = scale.dot(x) #apply scale
	x = transform.dot(x) #apply offset
	x = x.tolist()[:2] #remove additional component
	x = map(lambda x: int(x), x)
	x = tuple(x)
	return x

#reverse transformations of t (buggy)
def t_inverse(x):
	if (type(x) != np.ndarray 
		and type(x) in [list, tuple]):
		x = np.array(x)
	else:
		raise Exception("neither array nor list " + str(type(x)))
	x = np.append(x, [1.0])
	x = np.linalg.inv(transform).dot(x)
	x = np.linalg.inv(scale).dot(x)
	x = x.tolist()[:2]
	x = map(lambda x: int(x), x)
	x = tuple(x)
	return x

def sgn(x):
	return 1.0 if (x > 0.0) else -1.0

def circleOffset(co):
	return map(lambda x: x-1, co)

#main game loop
while True:
	#clear screen
	wso.fill(whiteColor)
	#draw coordsystem
	pygame.draw.line(wso, greyColor, [0, wheight/2.0], [wwidth, wheight/2.0])
	pygame.draw.line(wso, greyColor, [wwidth/2.0, 0], [wwidth/2.0, wheight])
	
	#draw correction points
	for x in range(-40, 40, 1):
		for y in range(-40, 40, 1):			
			px = x / 10.0
			py = y / 10.0
			val = 1.0 * w[0] + px * w[1] + py * w[2]			
			if (val > 0.0):
				pygame.draw.circle(wso, greyColor, t((px, py)), 1, 0)


	#draw data
	for c in pointsRed:
		pygame.draw.circle(wso, redColor, t(c), 2, 0)
	for c in pointsBlue:
		pygame.draw.circle(wso, blueColor, t(c), 2, 0)

	#handle input
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEBUTTONUP:
			mx, my = event.pos
			if event.button == 1:
				if placingRed:
					pointsRed.append(t_inverse([mx, my]))
				else:
					pointsBlue.append(t_inverse([mx, my]))
			elif event.button == 3:
				placingRed = not placingRed
			elif event.button == 2:
				training = not training
				pygame.display.set_caption('Perceptron '+ str(training))

	#train perceptron
	if training and time() > timeNextStep:
		print("training!")
		print("b:", w[0])
		print("w1:", w[1])
		print("w2:", w[2])
		future_w = deepcopy(w)
		for point in pointsRed + pointsBlue:
			val = 1.0 * w[0] + point[0] * w[1] + point[1] * w[2]
			val = sgn(val)
			if (point in pointsBlue):				
				if (val > 0.0):
					print("One or more points of Class B(Blue) were wrong!")
					future_w[0] = future_w[0] - 1.0 * 1.0 #b
					future_w[1] = future_w[1] - 1.0 * point[0] #w1
					future_w[2] = future_w[2] - 1.0 * point[1] #w2
			else:				
				if (val <= 0.0):
					print("One or more points of Class A(Red) were wrong!")
					future_w[0] = future_w[0] - (-1.0) * 1.0 #b
					future_w[1] = future_w[1] - (-1.0) * point[0] #w1
					future_w[2] = future_w[2] - (-1.0) * point[1] #w2
		del(w) #unneccessary?
		w = future_w



		#timeNextStep = time() + 0.01
		training=False	
	#draw w (normal vector)
	pygame.draw.aaline(wso, yellowColor, t((0, w[0])), t((w[1], w[2]+w[0])))

	#draw perceptron vector
	def v(t):
		return -(w[1]/w[2])*t - (w[0]/w[2])

	pygame.draw.aaline(wso, blackColor, t((-4, v(-4))), t((4, v(4))))	



	pygame.display.update()
	fpsClock.tick(30)

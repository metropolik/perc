import pygame, sys
from pygame.locals import *
from time import time
from random import random
import numpy as np

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

pointsBlue = [(-0.4, 0.8), (-0.8, -0.2)] #-1 #A
pointsRed = [(0.3, 1.6), (-0.4, 1.5)] #1 #B
placingRed = True
training = False
timeNextStep = 0
w = [0, 1, -1]

transform = np.array([[1.0, 0.0, wwidth/2.0], 
					  [0.0, 1.0, wheight/2.0],
					  [0.0, 0.0, 1.0]])
scalef = 50.0
scale = np.array([[scalef, 0.0, 0.0],
				  [0.0, -scalef, 0.0],
				  [0.0, 0.0, 1.0]])
#print("Transform matrix: ", both)

def t(x):
	if (type(x) != np.ndarray 
		and type(x) in [list, tuple]):
		x = np.array(x)
	else:
		raise Exception("neither array nor list " + str(type(x)))		
	x = np.append(x, [1.0])	
	x = scale.dot(x)
	x = transform.dot(x)	
	x = x.tolist()[:2]
	x = map(lambda x: int(x), x)
	x = tuple(x)
	return x

def sgn(x):
	return 1.0 if (x > 0.0) else -1.0



while True:
	#clear screen
	wso.fill(whiteColor)
	#draw coordsystem
	pygame.draw.line(wso, greyColor, [0, wheight/2.0], [wwidth, wheight/2.0])
	pygame.draw.line(wso, greyColor, [wwidth/2.0, 0], [wwidth/2.0, wheight])

	for c in pointsRed:
		pygame.draw.circle(wso, redColor, t(c), 3, 0)
	for c in pointsBlue:
		pygame.draw.circle(wso, blueColor, t(c), 3, 0)

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEBUTTONUP:
			mx, my = event.pos
			if event.button == 1:
				if placingRed:
					pointsRed.append([mx, my])
				else:
					pointsBlue.append([mx, my])
			elif event.button == 3:
				placingRed = not placingRed
			elif event.button == 2:
				training = not training
				pygame.display.set_caption('Perceptron '+ str(training))
	if training and time() > timeNextStep:
		print("training")
		# for point in pointsRed:
		# 	val = 1.0*w[0] + point[0]*w[1] + point[1]*w[2]
		# 	val = sgn(val)
		# 	print("val", val)
		# 	for i, x in enumerate([1.0] + list(point)):
		# 		delta_w = learningRate*(1.0 - val)*x
		# 		w[i] = w[i] + delta_w
		# 		print(str(i), ":", str(delta_w))

		# for point in pointsBlue:
		# 	val = 1.0*w[0] + point[0]*w[1] + point[1]*w[2]
		# 	val = sgn(val)
		# 	for i, x in enumerate([1.0] + list(point)):
		# 		w[i] = w[i] + learningRate*(-1.0 - val)*x
		
		for point in pointsBlue: #A Klasse -1
			val = 1.0 * w[0] + point[0] * w[1] + point[1] * w[2]
			val = sgn(val)
			if (val > 0.0): #wrongly classified
				print("Awro blu")
				w[0] = w[0] - 1.0 * 1.0 #b
				w[1] = w[1] - 1.0 * point[0] #w1
				w[2] = w[2] - 1.0 * point[1] #w2				

		for point in pointsRed: #B Klasse 1
			val = 1.0 * w[0] + point[0] * w[1] + point[1] * w[2]
			val = sgn(val)
			if (val <= 0.0): #wrongly classified
				print("Brwo red")
				w[0] = w[0] - (-1.0) * 1.0 #b
				w[1] = w[1] - (-1.0) * point[0] #w1
				w[2] = w[2] - (-1.0) * point[1] #w2


		#timeNextStep = time() + 0.01
		training=False
	
	#draw w (normal vector)
	pygame.draw.line(wso, yellowColor, t((0, w[0])), t((w[1], w[2]+w[0])))

	#draw perceptron
	def v(t):
		return (-(w[2])*t, w[1]*t+w[0])

	pygame.draw.line(wso, blackColor, t(v(-40)), t(v(40)))	



	pygame.display.update()
	fpsClock.tick(30)

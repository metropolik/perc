import pygame, sys
from pygame.locals import *
from time import time
from random import random


pygame.init()
fpsClock = pygame.time.Clock()

wso = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Perceptron')

redColor = pygame.Color(255, 0, 0)
blueColor = pygame.Color(0, 0, 255)
whiteColor = pygame.Color(255, 255, 255)
blackColor = pygame.Color(0, 0, 0)
mx, my = 0, 0
learningRate = 1.0

pointsBlue = [(-0.4, 0.8), (-0.8, -0.2)] #-1 #A
pointsRed = [(0.3, 1.6), (-0.4, 1.5)] #1 #B
placingRed = True
training = False
timeNextStep = 0
w = [0, 1, -1]

def sgn(x):
	return 1.0 if (x > 0.0) else -1.0

while True:
	wso.fill(whiteColor)
	for c in pointsRed:
		pygame.draw.circle(wso, redColor, (int(c[0])*100, int(c[1])*100), 3, 0)
	for c in pointsBlue:
		pygame.draw.circle(wso, blueColor, (int(c[0])*100, int(c[1])*100), 3, 0)

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
		for point in pointsRed:
			val = 1.0*w[0] + point[0]*w[1] + point[1]*w[2]
			val = sgn(val)
			print("val", val)
			for i, x in enumerate([1.0] + point):
				delta_w = learningRate*(1.0 - val)*x
				w[i] = w[i] + delta_w
				print(str(i), ":", str(delta_w))

		for point in pointsBlue:
			val = 1.0*w[0] + point[0]*w[1] + point[1]*w[2]
			val = sgn(val)
			for i, x in enumerate([1.0] + point):
				w[i] = w[i] + learningRate*(-1.0 - val)*x
	
		#timeNextStep = time() + 0.01
		training=False

	#draw perceptron
	#w1 w2 sind die normale
	#w0 der y offset
	y = -800 * (w[1]/w[2]) + w[0]
	pygame.draw.line(wso, blackColor, (0, w[0]), (800, y))
	#print(w, y)



	pygame.display.update()
	fpsClock.tick(30)

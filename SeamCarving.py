from PIL import Image, ImageDraw
import numpy
import math

filename = "InitialImage-1.jpg"
image = Image.open(filename)
width, height = image.size

energy = numpy.zeros(image.size)

def energyFunction (e, x, y):
    if(x ==0 or y ==0 or x == width-1 or y == height - 1):
        e[x][y] = 1000
    else:
        up = image.getpixel((x,y-1))
        down = image.getpixel((x,y+1))
        left = image.getpixel((x-1,y))
        right = image.getpixel((x+1,y))
        deltaYSquare = ((up[0]-down[0])**2) + ((up[1]-down[1])**2) + ((up[2]-down[2])**2)
        deltaXSquare = ((left[0]-right[0])**2) + ((left[1]-right[1])**2) + ((left[2]-right[2])**2)
        e[x][y] = math.sqrt(deltaXSquare + deltaYSquare)


for i in range(width):
    for j in range(height):
        energyFunction(energy, i, j)

print(energy[300][200])

#pixVal = image.getpixel((0, 0))
#print(pixVal[0])

print("FOR REAL?!")

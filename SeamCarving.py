from PIL import Image, ImageDraw
import numpy as np
import math




def get_energy_matrix(image):
    
    width, height = image.size

    energy_matrix = np.zeros(image.size)

    for i in range(width):
        for j in range(height):
            energyFunction(energy_matrix, i, j, width, height)
    
    return energy_matrix



def energyFunction (e, x, y, width, height):
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




"""
auxillary_matrices: creates solution_matrix with min paths' costs and path_matrix


INPUTS
energy_matrix: a matrix of energies for each pixel in the image

OUTPUTS
solution_matrix: the matrix of min paths' costs that helps us figure out 
                 the actual path
path_matrix: the matrix of -1,0,1 that helps us figure out the actual path
"""
def auxillary_matrices(energy_matrix):
    rows = energy_matrix.shape[0]
    cols = energy_matrix.shape[1]

    solution_matrix = np.zeros((rows, cols))
    path_matrix = np.arange(rows*cols).reshape((rows,cols))

    min_energy = math.inf

    # USE BOTTOM - UP APPROACH

    #start at the last row, just copy the last row of energy matrix
    solution_matrix[rows-1, 0:] = energy_matrix[rows-1, 0:]


    for row in range(rows-2, -1, -1):
        for col in range(cols):

            # figure out left, right, down
            left = math.inf
            right = math.inf
            if (col != 0): # not in first column, check left
                left = energy_matrix[row, col] + solution_matrix[row+1, col-1]
            
            if (col != cols-1): # not in last column, check right
                right = energy_matrix[row, col] + solution_matrix[row+1, col+1]

            down = energy_matrix[row, col] + solution_matrix[row+1, col]


            # find optimal solution
            solution = min(left, down, right)
            solution_matrix[row, col] = solution

            # figure out the path and record it in path_matrix
            if (solution == left):
                path_matrix[row, col] = -1
            elif (solution == right):
                path_matrix[row, col] = 1
            else:
                path_matrix[row, col] = 0

            '''
            storing paths:
            left: -1
            down: 0 
            right: 1
            '''


    return solution_matrix, path_matrix




"""
get_seam: creates a list of coordinates for pixels that are to be removed

INPUTS
solution_matrix: a matrix of optimal solutions for each pixel
path_matrix: a matrix of paths that corresponds to optimal solutions

OUTPUTS
seam: a list of coordinates of pixels to be removed
"""
def get_seam(solution_matrix, path_matrix):
    
    rows = solution_matrix.shape[0]
    cols = solution_matrix.shape[1]

    row = 0
    
    min_value_index = 0
    for i in range(cols):
        if (solution_matrix[0, i] < solution_matrix[0, min_value_index]):
            min_value_index = i

    col = min_value_index
    print("column")
    print(col)
    print()
    seam = []

    while (row < rows):
        seam.append((row, col))
        col += path_matrix[row, col]
        row += 1
    
    return seam
        


def reduce_image(image, seam):
    return





"""
Python's "main function" block.
"""
if __name__ == "__main__":

    filename = "InitialImage-1.jpg"
    image = Image.open(filename)

    energy_matrix = get_energy_matrix(image)

    print(energy_matrix[300][200])
    print(energy_matrix[0][200])


    # test_energy_matrix = np.array([[8,3,4],
    #                             [2,10,1],
    #                             [9,2,5]])

    # print(test_energy_matrix)

    solution_matrix, path_matrix = auxillary_matrices(energy_matrix)


    print()
    print(solution_matrix)
    print()
    print(path_matrix)


    seam = get_seam(solution_matrix, path_matrix)




    print()
    print(seam)
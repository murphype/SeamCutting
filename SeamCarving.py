from PIL import Image, ImageDraw
import numpy as np
import math


#CONSTANTS
FILENAME = "InitialImage-1.jpg"
DESIRED_WIDTH = 408



'''
get_energy_matrix: constructs a matrix of energies for each pixel where energy is related
to how similar each pixel is to its neighbouring pixels

INPUTS:
image: the image

OUTPUTS:
energy_matrix: the energy matrix
'''
def get_energy_matrix(image):
    
    width, height = image.size
    #declare the energy matrix
    energy_matrix = np.zeros((height, width))
    
    # fill in the energy matrix, one entry/pixel at a time
    for i in range(width):
        for j in range(height):
            energyFunction(energy_matrix, i, j, width, height, image)
    
    return energy_matrix



'''
energyFunction: gets an energy for a specific pixel

INPUTS:
e: energy matrix
x: row index of the pixel
y: column index of the pixel
width: width of the image / energy matrix
height: height of the image / energy matrix
image: the image

OUTPUTS:
none, modifies the energy matrix directly
'''
def energyFunction (e, x, y, width, height, image):
    if(x ==0 or y ==0 or x == width-1 or y == height - 1):
        e[y][x] = 1000
    else:
        #get rgb values for up, down, left, right pixels
        up = image.getpixel((x,y-1))
        down = image.getpixel((x,y+1))
        left = image.getpixel((x-1,y))
        right = image.getpixel((x+1,y))
        #calculate the differences in vertical and horizontal directions
        deltaYSquare = ((up[0]-down[0])**2) + ((up[1]-down[1])**2) + ((up[2]-down[2])**2)
        deltaXSquare = ((left[0]-right[0])**2) + ((left[1]-right[1])**2) + ((left[2]-right[2])**2)
        # update the energy matrix
        e[y][x] = math.sqrt(deltaXSquare + deltaYSquare)



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
    # find the startinf point of the seam from the first row of the solution matrix
    for i in range(cols):
        if (solution_matrix[0, i] < solution_matrix[0, min_value_index]):
            min_value_index = i

    col = min_value_index
    # declare the seam as a list of coordinates corresponding to pixels
    seam = []

    # iterate through each row
    while (row < rows):
        # use path matrix to append the next pixel to seam
        seam.append((row, col))
        col += path_matrix[row, col]
        row += 1
    
    return seam
        


"""
delete_seam: reduces an image by cutting out a vertical seam

INPUTS
image: an image object to be reduced 
seam: a vector of coordinates representing the seam to be removed

OUTPUTS
image: the reduced image
"""
def delete_seam(image, seam):
    # transform the image object into a 3d array
    img = np.array(image).astype(int)
    

    # create a boolean mask of the img matrix
    mask = np.ones(img.shape, dtype=bool)

    # for every pixel in the seam, set the correspoding mask's matrix to false
    for pixel in seam:
        mask[pixel[0],pixel[1], :] = False


    # reconstruct the img matrix by omitting the corresponding false values
    # using the mask matrix
    img = img[mask].reshape(img.shape[0], img.shape[1]-1, 3)
    # print(img.shape)
    
    # put the image object back together with the seam deleted
    image1 = Image.fromarray(img.astype(np.uint8), mode = "RGB")
    return image1



'''
seam_carve: the driving function that iteratively reduces one seams from image

INPUTS:
image: the image to be reduced
desired_width: the desired width dimension of the image

OUTPUTS:
image: the reduced image
'''
def seam_carve(image, desired_width):
    #define number of needed iterations
    iter = image.size[0] - desired_width

    # for loop to delete one seam at a time
    for i in range(iter):
        print("iteration:", i)

        #get energy matrix
        energy_matrix = get_energy_matrix(image)

        # get solution_matrix and path_matrix
        solution_matrix, path_matrix = auxillary_matrices(energy_matrix)

        # get the seam to delete
        seam = get_seam(solution_matrix, path_matrix)

        # update the image by deleting the seam
        image = delete_seam(image, seam)
    
    return image



"""
Python's "main function" block.
"""
if __name__ == "__main__":
    image = Image.open(FILENAME)
    image = seam_carve(image, DESIRED_WIDTH)
    image.save("FinalImage.jpg")

        
            



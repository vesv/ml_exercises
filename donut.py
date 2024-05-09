import pygame
import math
import colorsys

pygame.init() #initialize pygame

black = (0, 0, 0) #background color
white = (255, 255, 255) #text color
hue = 0 #hue value

height = 1080 #window sizes
width = 1920

x_start, y_start = 0, 0 #starting position of text
x_seperation, y_seperation = 10, 20 
rows = height // y_seperation #rows and columns
cols = width // x_seperation
screen_size = rows * cols
x_offset = cols / 2 #offsets
y_offset = rows / 2

A, B = 0, 0  #angles

theta_spacing = 10 #angle spacing
phi_spacing = 1 

chars = ".,-~:;=!*#$@" #ascii chars for illumination

screen = pygame.display.set_mode((width, height)) 
display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 
pygame.display.set_caption("Donut")
font = pygame.font.SysFont('Helvetica', 18, bold=True) #font

#the purpose of this code is to generate a torus in 3D using ascii characters
#the way it works is by calculating the position of each point on the torus
#then it calculates the illumination of each point
#then it uses the illumination to determine which ascii character to use

def hsv_converter(h, s, v): #converts hsv to rgb
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

def text_display(letter, x_start, y_start):
    text = font.render(str(letter), True, hsv_converter(hue, 1, 1)) 
    display_surface.blit(text, (x_start, y_start))


run = True
while run:
    screen.fill((black))

    z = [0] * screen_size #the donut itself
    b = [' '] * screen_size #background which fills empty space

    #to project a 3d object on a 2d screen, we project each point (x, y, z) in 3d space onto a 2d plane z' units away from the viewer
    #so that the relative 2d position is (x', y')
    #to project a 3d coordinate to 2d, the coordinate is scaled by z'
    #z' can be chosen based on the intended POV of the viewer
    
    for j in range(0, 628, theta_spacing):  
        for i in range(0, 628, phi_spacing): 
            c = math.sin(i) 
            d = math.cos(j) 
            e = math.sin(A) 
            f = math.sin(j)
            g = math.cos(A) 
            h = d + 2
            D = 1 / (c * h * e + f * g + 5)
            l = math.cos(i)
            m = math.cos(B)
            n = math.sin(B)
            t = c * h * g - f * e
            x = int(x_offset + 40 * D * (l * h * m - t * n))
            y = int(y_offset + 20 * D * (l * h * n + t * m))
            o = int(x + cols * y)
            N = int(8 * ((f * e - c * d * g) * m - c * d * e - f * g - l * d * n)) 
            if rows > y and y > 0 and x > 0 and cols > x and D > z[o]:
                z[o] = D
                b[o] = chars[N if N > 0 else 0]

    #when plotting points, it's possible to plot different points at the same (x', y') location but at different depths
    #for this purpose we use the z-buffer to store the depth of each point
    #when plotting a location, we check if the depth of the new point is greater than the depth of the point already plotted

    #plotting the donut/torus itself is simple
    #this can be done by drawing a 2d circle around a point in 3d space, and then rotate it around the central axis of the torus
    #a circle of radius R1 centered at (R2, 0, 0) drawn on the xy-plane. this can be done by sweeping an angle from 0 to 2pi
    #the circle is then rotated around the y-axis by a different angle using the rotation matrix
    #the torus is then projected onto a 2d plane to get the final image

    #in order to achieve the desired animation, the donut needs to be rotated around 2 more axes
    #which is just a matter of matrix multiplication

    #to calculate illumination we need to know the direction perpendicular to the surface at every point
    #we can take the the dot product of that value and the light source to get the illumination
    #it gives us the cosine of the angle between the light direction and the surface direction
    #if the dot product is >0, the surface is facing the light, and if <0, the surface is facing away from the light
    #illumination increases with the value

    if y_start == rows * y_seperation - y_seperation:
        y_start = 0

    for i in range(len(b)):
        A += 0.000002
        B += 0.000001
        if i == 0 or i % cols:
            text_display(b[i], x_start, y_start)
            x_start += x_seperation
        else:
            y_start += y_seperation
            x_start = 0
            text_display(b[i], x_start, y_start)
            x_start += x_seperation

    pygame.display.update() 

    hue += 0.002 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

import pygame
from pygame.locals import * # Import all Pygame constants
from OpenGL.GL import *
from OpenGL.GLU import *
import mesh
# import Rendere  # We will create a new OpenGL-based renderer

# --- Initialization ---
pygame.init()

# --- Screen Setup ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen_dimensions = (SCREEN_WIDTH, SCREEN_HEIGHT)

# --- Create the OpenGL-enabled display ---
# 1. Add the OPENGL and DOUBLEBUF flags
flags = OPENGL | DOUBLEBUF
screen = pygame.display.set_mode(screen_dimensions, flags)

# Set the window title
pygame.display.set_caption("3D Rendering with OpenGL")

# --- NEW OPENGL SETUP ---
# 2. Enable the depth buffer (Z-buffer)
glEnable(GL_DEPTH_TEST)

# 3. Set up the 3D perspective
glMatrixMode(GL_PROJECTION)
# field of view, aspect ratio, near clip plane, far clip plane
gluPerspective(45, (SCREEN_WIDTH / SCREEN_HEIGHT), 0.1, 100.0) 

# 4. Move the "camera" back so we can see
glMatrixMode(GL_MODELVIEW)
# Move 5 units back (out of the screen)
glTranslate(0.0, 0.0, -5.0) 
# --- END NEW OPENGL SETUP ---

# --- Comment out the old renderer ---
# Your old renderer class draws to the CPU (Pygame surface)
# It cannot draw to an OpenGL context.
# renderer = Rendere.Renderer(screen, SCREEN_WIDTH, SCREEN_HEIGHT, focal = 500)

# --- Main Game Loop ---
running = True
clock = pygame.time.Clock()

# You can still load the mesh data, this is perfect
shape = mesh.mesh("bulb.stl")

def drawScene():
    # 5. Clear the screen (Color and Depth buffers)
    # This replaces 'screen.fill(WHITE)'
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # --- Your new OpenGL drawing code will go here ---
    # (e.g., bind shaders, set uniforms, draw VBO)
    
    # --- Old code commented out ---
    # renderer.drawCube(screen, shape,wire=True)

def inputSystem(mesh):
    keys = pygame.key.get_pressed()
    
    # This input system is 100% perfect and does not need to change.
    # It modifies the 'shape' object's properties in Python.
    # Our new renderer will read these values (shape.rotation, etc.)
    # and send them to the GPU.
    
    if keys[pygame.K_w]:
        mesh.position[2] += 0.1
    if keys[pygame.K_a]:
        mesh.position[0] -= 0.1
    if keys[pygame.K_s]:
        mesh.position[2] -= 0.1
    if keys[pygame.K_d]:
        mesh.position[0] += 0.1
    if keys[pygame.K_SPACE]:
        mesh.position[1] += 0.1
    if keys[pygame.K_LSHIFT]:
        mesh.position[1] -= 0.1
    if keys[pygame.K_LEFT]:
        mesh.rotateY(-0.1)
    if keys[pygame.K_RIGHT]:
        mesh.rotateY(0.1)
    if keys[pygame.K_UP]:
        mesh.rotateX(0.1)
    if keys[pygame.K_DOWN]:
        mesh.rotateX(-0.1)
    if keys[pygame.K_e]:
        mesh.rotateZ(0.1)
    if keys[pygame.K_x]:
        mesh.rotateZ(-0.1)


while running:
    # --- Event Processing ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    inputSystem(shape)
    drawScene()

    # 6. 'flip' now swaps the hidden OpenGL buffer with the visible one
    pygame.display.flip()
    clock.tick(60)

# --- Quit Pygame ---
pygame.quit()
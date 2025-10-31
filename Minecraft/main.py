import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import mesh
import openGLRenderer  # <-- Import the new renderer

# --- Initialization ---
pygame.init()

# --- Screen Setup ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen_dimensions = (SCREEN_WIDTH, SCREEN_HEIGHT)

# --- Create the OpenGL-enabled display ---
flags = OPENGL | DOUBLEBUF
screen = pygame.display.set_mode(screen_dimensions, flags)
pygame.display.set_caption("3D Rendering with OpenGL")

# --- NEW OPENGL SETUP ---
glEnable(GL_DEPTH_TEST) # Replaces your Z-sort (Painter's Algorithm)
glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT) # Tell OpenGL the size of the window

# --- Create the new Renderer ---
# This will compile the shaders
renderer = openGLRenderer.OpenGLRenderer(SCREEN_WIDTH, SCREEN_HEIGHT)

# --- Main Game Loop ---
running = True
clock = pygame.time.Clock()

# Load the mesh data (this is perfect, no changes)
shape = mesh.mesh("bulb.stl")

# --- UPLOAD MESH TO GPU (ONE-TIME) ---
renderer.upload_mesh(shape)

def drawScene(mesh_obj):
    # Clear the screen (Color and Depth buffers)
    glClearColor(0.1, 0.1, 0.1, 1.0) # A dark grey background
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # --- Tell the new renderer to draw ---
    renderer.draw(mesh_obj)

def inputSystem(mesh):
    # --- NO CHANGES NEEDED ---
    # This code is perfect. It modifies the 'shape'
    # object's properties on the CPU. The renderer
    # will read these properties each frame.
    keys = pygame.key.get_pressed()
    
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
    drawScene(shape) # Pass the shape to the draw function

    pygame.display.flip()
    clock.tick(60)

# --- Quit Pygame ---
pygame.quit()
import pygame
import mesh
import Rendere


# --- Initialization ---
pygame.init()

# --- Screen Setup ---
# Set the width and height of the screen (in pixels)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen_dimensions = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Create the display surface
screen = pygame.display.set_mode(screen_dimensions)

# Set the window title
pygame.display.set_caption("3D Rendering")

# --- Define Colors (RGB) ---
WHITE = (255, 255, 255)
RED = (255, 0, 0)

renderer = Rendere.Renderer(screen, SCREEN_WIDTH, SCREEN_HEIGHT, focal = 500)

# --- Main Game Loop ---
running = True
clock = pygame.time.Clock()
x = SCREEN_WIDTH /2
y = SCREEN_HEIGHT / 2


shape = mesh.mesh("cube.json")

def drawScene():
    screen.fill(WHITE)
    #renderer.drawCube(screen, cube1,wire=True, solid=True)
    #renderer.drawCube(screen, pyramid)
    renderer.drawCube(screen, shape,wire=False,solid=True)

def inputSystem(mesh):
    keys = pygame.key.get_pressed()
    
    # Check for continuous key presses
    if keys[pygame.K_w]:
        print("'w' key held down")
        # Add your 'w' key logic here
        mesh.position[2] += 0.1
        pass
    if keys[pygame.K_a]:
        print("'a' key held down")
        # Add your 'a' key logic here
        mesh.position[0] -= 0.1
        pass
    if keys[pygame.K_s]:
        print("'s' key held down")
        # Add your 's' key logic here
        mesh.position[2] -= 0.1
        pass    
    if keys[pygame.K_d]:
        print("'d' key held down")
        # Add your 'd' key logic here
        mesh.position[0] += 0.1
        pass
    if keys[pygame.K_SPACE]:
        print("'SPACE' key held down")
        # Add your 'd' key logic here
        mesh.position[1] += 0.1
        pass
    if keys[pygame.K_LSHIFT]:
        print("'LSHIFT' key held down")
        # Add your 'd' key logic here
        mesh.position[1] -= 0.1
        pass
    if keys[pygame.K_LEFT]:
        print("'LEFT' key held down")
        # Add your 'd' key logic here
        mesh.rotateY(-0.1)
        pass
    if keys[pygame.K_RIGHT]:
        print("'RIGHT' key held down")
        # Add your 'd' key logic here
        mesh.rotateY(0.1)
        pass
    if keys[pygame.K_UP]:
        print("'UP' key held down")
        # Add your 'd' key logic here
        mesh.rotateX(0.1)
        pass
    if keys[pygame.K_DOWN]:
        print("'DOWN' key held down")
        # Add your 'd' key logic here
        mesh.rotateX(-0.1)
        pass
    if keys[pygame.K_e]:
        print("'e' key held down")
        # Add your 'd' key logic here
        mesh.rotateZ(0.1)
        pass
    if keys[pygame.K_x]:
        print("'x' key held down")
        # Add your 'd' key logic here
        mesh.rotateZ(-0.1)
        pass


while running:
    # --- Event Processing ---
    for event in pygame.event.get():
        
        # 1. Check for the QUIT event (clicking the window's 'X' button)
        if event.type == pygame.QUIT:
            running = False  # Exit the loop

    inputSystem(shape)
    drawScene()

    pygame.display.flip()
    clock.tick(60)

# --- Quit Pygame ---
pygame.quit()
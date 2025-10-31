import pygame
import sys

pygame.init()

# --- Screen Setup ---
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)   # Vertical lines
RED = (255, 0, 0)     # Horizon line
BLUE = (0, 0, 255)    # Horizontal lines

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Perspective Grid")

# --- Perspective Controls ---
bottom_spacing_x = 80  # Spacing at bottom (vertical lines)
horizon_spacing_x = 20 # Spacing at horizon (vertical lines)
bottom_spacing_y = 30  # Spacing for the *first* horizontal line from the bottom

# --- Y-Axis Positions ---
horizon_y = HEIGHT // 2
bottom_y = HEIGHT

# --- Calculations ---
center_x = WIDTH // 2
spread_ratio_x = bottom_spacing_x / max(1, horizon_spacing_x)

# --- Main Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Colors ---
    SKY_BLUE = (135, 206, 235)
    GROUND_GREEN = (34, 139, 34)
    # ... inside the main loop, right after screen.fill(BLACK)

    # Draw Sky
    pygame.draw.rect(screen, SKY_BLUE, (0, 0, WIDTH, horizon_y))
    # Draw Ground
    pygame.draw.rect(screen, GROUND_GREEN, (0, horizon_y, WIDTH, HEIGHT - horizon_y))

    # --- Draw Vertical Grid Lines ---
    # (Your code here...)

    # --- Draw Vertical Grid Lines ---
    for x_horizon in range(0, WIDTH + 1, horizon_spacing_x):
        offset_from_center = x_horizon - center_x
        x_bottom = center_x + (offset_from_center * spread_ratio_x)
        pygame.draw.line(screen, GREEN, (x_bottom, bottom_y), (x_horizon, horizon_y), 1)

    # --- Draw Horizontal Grid Lines (Corrected Logic) ---
    
    # This is the total pixel distance from horizon to bottom
    total_vertical_distance = bottom_y - horizon_y
    
    # This is the Y-position of the line we are about to draw
    current_y = bottom_y
    
# --- Main Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK) # Clear screen

    # --- STEP 1: Draw Horizontal Lines (FIRST) ---
    
    total_vertical_distance = bottom_y - horizon_y
    current_y = bottom_y
    
    # This will store the Y-value of the very last line we draw
    top_of_grid_y = bottom_y 
    
    while current_y > horizon_y:
        pygame.draw.line(screen, BLUE, (0, int(current_y)), (WIDTH, int(current_y)), 1)
        
        # We just drew a line, so save its position as the "top"
        top_of_grid_y = int(current_y) 
        
        distance_ratio = (current_y - horizon_y) / max(1, total_vertical_distance)
        dy = bottom_spacing_y * distance_ratio
        
        if dy < 1.5:
            break # Stop drawing, top_of_grid_y is now set
            
        current_y -= dy

    # --- STEP 2: Draw Vertical Grid Lines (SECOND) ---
    
    # This is the total Y-distance of our grid
    total_grid_y_span = bottom_y - horizon_y
    if total_grid_y_span <= 0: total_grid_y_span = 1 # Avoid divide-by-zero
        
    for x_horizon in range(0, WIDTH + 1, horizon_spacing_x):
        offset_from_center = x_horizon - center_x
        x_bottom = center_x + (offset_from_center * spread_ratio_x)
        
        # --- This is the new calculation ---
        # We need to find the correct X-position for our line
        # at 'top_of_grid_y'. We use linear interpolation (lerp).
        
        # Find how "far up" our grid top is (0.0 = bottom, 1.0 = horizon)
        t = (bottom_y - top_of_grid_y) / total_grid_y_span
        
        # Use that 't' value to find the matching X-coordinate
        # (1 - t) * start_x + t * end_x
        x_top = (1 - t) * x_bottom + t * x_horizon
        
        # Draw the line to the new, corrected top point
        pygame.draw.line(screen, GREEN, (x_bottom, bottom_y), (x_top, top_of_grid_y), 1)

    # --- Draw the horizon line (LAST) ---
    # This draws ON TOP of the grid for a clean edge
    pygame.draw.line(screen, RED, (0, horizon_y), (WIDTH, horizon_y), 1)

    pygame.display.flip()

pygame.quit()
sys.exit()
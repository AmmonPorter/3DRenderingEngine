import pygame
import math
import math_utils

class Renderer():
    def __init__(self, screen, screenWidth, screenHeight, focal = 300):
        self.focalLength = focal
        self.screen = screen
        self.width = screenWidth
        self.height = screenHeight
        self.light_vector = (0,0,-1)

    def project3DTo2D(self,x,y,z):
        centerX = self.width / 2
        centerY = self.height / 2
        cameraZ = -5

        zDistance = z - cameraZ
        projectedX = (x * self.focalLength) / zDistance
        projectedY = (y * self.focalLength) / zDistance

        screenX = projectedX + centerX
        screenY = -projectedY + centerY
        coords = [screenX, screenY]
        return coords

    def drawCube(self, screen, mesh, color=(0,255,0), solid = False, wire = True):
        final_world_vertices = []

        x_angle = mesh.rotation[0]
        y_angle = mesh.rotation[1]
        z_angle = mesh.rotation[2]
        x_sin = math.sin(x_angle)
        x_cos = math.cos(x_angle)
        y_sin = math.sin(y_angle)
        y_cos = math.cos(y_angle)
        z_sin = math.sin(z_angle)
        z_cos = math.cos(z_angle)

        for verticy in mesh.vertices:
            # (Get base x, y, z)
            x, y, z = verticy
            
            # (Do all your X, Y, Z rotation math here...)
            # x Rotation
            x1 = x
            y1 = y * x_cos - z * x_sin
            z1 = y * x_sin + z * x_cos
            # y Rotation
            x2 = x1 *y_cos - z1 * y_sin
            y2 = y1
            z2 = x1 * y_sin + z1 *y_cos
            # z Rotation
            x3 = x2 * z_cos - y2 * z_sin
            y3 = x2 * z_sin + y2 * z_cos
            z3 = z2
            
            # --- NOW, ADD TRANSLATION (POSITION) ---
            final_x = x3 + mesh.position[0]
            final_y = y3 + mesh.position[1]
            final_z = z3 + mesh.position[2]

            # Save the final 3D point
            final_world_vertices.append( (final_x, final_y, final_z) )
            
        

        if solid:
            self.renderSolid(screen, mesh, color, final_world_vertices)
        
        if wire:
            self.renderWire(screen, mesh, color, final_world_vertices)
        
    def renderSolid(self, screen, mesh, color, final_world_vertices):
        
        light_direction = (0, 0, -1)
        faces_to_render = []

        for face in mesh.triangles:
            # 1. Get 3D Vertices
            A = final_world_vertices[face[0]]
            B = final_world_vertices[face[1]]
            C = final_world_vertices[face[2]]

            # 2. Calculate Lighting
            v1 = (B[0] - A[0], B[1] - A[1], B[2] - A[2])
            v2 = (C[0] - A[0], C[1] - A[1], C[2] - A[2])
            normal = math_utils.crossProduct(v1, v2)
            normal = math_utils.normalize(normal)
            brightness = math_utils.dotProduct(normal, light_direction)

            # --- Don't draw yet! ---
            # 3. Calculate Average Depth (for sorting)
            avg_z = (A[2] + B[2] + C[2]) / 3
            
            # 4. Project 2D points
            pA = self.project3DTo2D(A[0], A[1], A[2])
            pB = self.project3DTo2D(B[0], B[1], B[2])
            pC = self.project3DTo2D(C[0], C[1], C[2])
            face_points = [pA, pB, pC]
            
            # 5. Store all data for this face
            faces_to_render.append( (avg_z, face_points, brightness) )

        # --- SORTING STEP (Painter's Algorithm) ---
        # Sort the list by 'avg_z' (item 0) from high to low (far to near)
        faces_to_render.sort(key=lambda f: f[0], reverse=True)
        ambient_light = .05
        # --- FINAL DRAWING LOOP ---
        for avg_z, face_points, brightness in faces_to_render:
            brightness = abs(brightness)
            final_brightness = min(1.0, brightness + ambient_light)
            final_color = (
                int(color[0] * final_brightness), 
                int(color[1] * final_brightness), 
                int(color[2] * final_brightness)
            )
            pygame.draw.polygon(screen, final_color, face_points)


    def renderWire(self, screen, mesh, color, final_world_vertices):
        color = (255,0,0) 

        for face in mesh.triangles:
            # Get the 3D points
            A = final_world_vertices[face[0]]
            B = final_world_vertices[face[1]]
            C = final_world_vertices[face[2]]

            # Project them to 2D
            pA = self.project3DTo2D(A[0], A[1], A[2])
            pB = self.project3DTo2D(B[0], B[1], B[2])
            pC = self.project3DTo2D(C[0], C[1], C[2])
            
            # Draw the 3 lines of the triangle
            pygame.draw.line(screen, color, pA, pB)
            pygame.draw.line(screen, color, pB, pC)
            pygame.draw.line(screen, color, pC, pA)

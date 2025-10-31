import pygame
from OpenGL.GL import *
import numpy as np
import pyrr # This is our new math library

class OpenGLRenderer:
    def __init__(self, screen_width, screen_height):
        
        # --- 1. Compile Shaders and Link Program ---
        try:
            vertex_code = self._load_shader_file("vertex_shader.glsl")
            fragment_code = self._load_shader_file("fragment_shader.glsl")
            
            vertex_shader = self._compile_shader(vertex_code, GL_VERTEX_SHADER)
            fragment_shader = self._compile_shader(fragment_code, GL_FRAGMENT_SHADER)
            
            self.shader_program = self._link_program(vertex_shader, fragment_shader)
        except Exception as e:
            print(f"Error during shader setup: {e}")
            raise

        # --- 2. Create VAO, VBO, and EBO ---
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)
        self.triangle_count = 0

        # --- 3. Create Projection and View Matrices ---
        # These replace your 'project3DTo2D' and 'cameraZ'
        
        # PROJECTION matrix: (Our 3D "camera lens")
        # 45-degree field of view, aspect ratio, near clip plane, far clip plane
        self.projection_matrix = pyrr.matrix44.create_perspective_projection(
            45.0, screen_width / screen_height, 0.1, 100.0
        )
        
        # VIEW matrix: (Our "camera" position)
        # We place the camera at (0, 0, 5) looking at (0, 0, 0)
        self.view_matrix = pyrr.matrix44.create_look_at(
            pyrr.Vector3([0.0, 0.0, 5.0]), # Eye (camera) position
            pyrr.Vector3([0.0, 0.0, 0.0]), # Target to look at
            pyrr.Vector3([0.0, 1.0, 0.0])  # "Up" vector
        )

        # Get the "location" of the uniforms in the shader
        # This is how we send data (like our matrices) to the GPU
        self.model_loc = glGetUniformLocation(self.shader_program, "model")
        self.view_loc = glGetUniformLocation(self.shader_program, "view")
        self.proj_loc = glGetUniformLocation(self.shader_program, "projection")


    def upload_mesh(self, mesh):
        # "Bind" the VAO (activate it)
        glBindVertexArray(self.vao)

        # --- Upload Vertex Data (VBO) ---
        vertices = np.array(mesh.vertices, dtype=np.float32)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # --- Upload Index Data (EBO) ---
        indices = np.array(mesh.triangles, dtype=np.uint32)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        
        # Store how many points we need to draw
        self.triangle_count = len(indices.flatten()) # Total number of indices

        # --- Configure Vertex Attributes ---
        # This tells the shader how to read the VBO
        # (Attribute 0, 3 floats (x,y,z), don't normalize, 
        #  12-byte stride (3 floats * 4 bytes each), 
        #  0 offset)
        glEnableVertexAttribArray(0) # layout (location = 0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))

        # Unbind (good practice)
        glBindVertexArray(0)
        print(f"Mesh uploaded to GPU: {self.triangle_count // 3} triangles.")


    def draw(self, mesh):
        
        # --- 1. Activate Shader Program ---
        glUseProgram(self.shader_program)
        
        # --- 2. Create Model Matrix (Rotation & Translation) ---
        # This replaces all your old 'x_sin', 'y_cos' math
        
        # Start with an identity matrix (a blank slate)
        model_matrix = pyrr.matrix44.create_identity()
        
        # Apply your rotations (from mesh.rotation)
        model_matrix = pyrr.matrix44.multiply(
            model_matrix,
            pyrr.matrix44.create_from_z_rotation(mesh.rotation[2])
        )
        model_matrix = pyrr.matrix44.multiply(
            model_matrix,
            pyrr.matrix44.create_from_y_rotation(mesh.rotation[1])
        )
        model_matrix = pyrr.matrix44.multiply(
            model_matrix,
            pyrr.matrix44.create_from_x_rotation(mesh.rotation[0])
        )
        
        # Apply your translation (from mesh.position)
        model_matrix = pyrr.matrix44.multiply(
            model_matrix,
            pyrr.matrix44.create_from_translation(mesh.position)
        )

        # --- 3. Send Matrices to the GPU Shaders ---
        # This is where your Python code "talks" to the GLSL code
        glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, self.projection_matrix)
        glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, self.view_matrix)
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, model_matrix)

        # --- 4. Activate the VAO and Draw ---
        glBindVertexArray(self.vao)
        
        # This is the ONE command that draws everything
        glDrawElements(GL_TRIANGLES, self.triangle_count, GL_UNSIGNED_INT, None)

        # --- 5. Clean up ---
        glBindVertexArray(0)
        glUseProgram(0)


    # --- (Helper Functions for Compiling Shaders) ---

    def _load_shader_file(self, filename):
        with open("Minecraft/"+filename, 'r') as file:
            return file.read()

    def _compile_shader(self, source_code, shader_type):
        shader_id = glCreateShader(shader_type)
        glShaderSource(shader_id, source_code)
        glCompileShader(shader_id)
        if not glGetShaderiv(shader_id, GL_COMPILE_STATUS):
            error_message = glGetShaderInfoLog(shader_id).decode('utf-8')
            glDeleteShader(shader_id)
            raise RuntimeError(f"Shader compilation failed: {error_message}")
        return shader_id

    def _link_program(self, vertex_shader_id, fragment_shader_id):
        program_id = glCreateProgram()
        glAttachShader(program_id, vertex_shader_id)
        glAttachShader(program_id, fragment_shader_id)
        glLinkProgram(program_id)
        if not glGetProgramiv(program_id, GL_LINK_STATUS):
            error_message = glGetProgramInfoLog(program_id).decode('utf-8')
            glDeleteProgram(program_id)
            raise RuntimeError(f"Shader program linking failed: {error_message}")
        glDeleteShader(vertex_shader_id)
        glDeleteShader(fragment_shader_id)
        return program_id
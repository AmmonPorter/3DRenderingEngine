#version 330 core

// This is the vertex position (x, y, z) coming in from your VBO
layout (location = 0) in vec3 aPos;

// These are the matrices we will get from our Python code
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    // This is the core formula of 3D graphics.
    // It multiplies the vertex position by all the matrices
    // to get the final position on the screen.
    gl_Position = projection * view * model * vec4(aPos, 1.0);
}
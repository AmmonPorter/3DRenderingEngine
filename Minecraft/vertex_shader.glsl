#version 330 core

// This is the vertex position (x, y, z) coming in from your VBO
layout (location = 0) in vec3 aPos;

void main()
{
    // gl_Position is a special built-in variable.
    // This is the final 2D position you are outputting.
    // We just pass the 3D position through as a 4D point (w=1.0).
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
}
#version 330 core

// This is the final color you are outputting
out vec4 FragColor;

void main()
{
    // We set the output color to Red.
    // Colors are in (R, G, B, Alpha) format,
    // with values from 0.0 to 1.0.
    FragColor = vec4(1.0, 0.0, 0.0, 1.0); // Solid Red
}
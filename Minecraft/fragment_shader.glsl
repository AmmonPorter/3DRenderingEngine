#version 330 core

// This is the final color we are outputting
out vec4 FragColor;

void main()
{
    // We set the output color to a solid red.
    // (We will add lighting math back in here later)
    FragColor = vec4(1.0, 0.0, 0.0, 1.0); // Solid Red
}
import math

#Finds the normals of a face
def crossProduct(v1, v2):
    x = (v1[1] * v2[2] - v1[2] * v2[1])
    y = (v1[2] * v2[0] - v1[0] * v2[2])
    z = (v1[0] * v2[1] - v1[1] * v2[0])
    return (x, y, z)

def normalize(v):
    x, y, z = v
    length = math.sqrt(x*x + y*y + z*z)
    
    # --- THIS IS THE BUG ---
    # You MUST check if length is near zero
    if length < 0.001:
        return (0, 0, 0) # Return a VALID vector
    
    return (x / length, y / length, z / length)

def dotProduct(v1, v2):
    result = (v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2])
    return result

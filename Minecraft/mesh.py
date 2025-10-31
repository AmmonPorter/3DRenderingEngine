import math
import json

class mesh:
    def __init__(self, mesh):
        if ".json" in mesh:
            self.loadJson(mesh)



        self.position = [0,0,0]
        self.rotation = [0,0,0]
    
    def rotateX(self, angle):
        self.rotation[0] += angle
        self.rotation[0] = self.rotation[0] % math.tau

    def rotateY(self, angle):
        self.rotation[1] += angle
        self.rotation[1] = self.rotation[1] % math.tau

    def rotateZ(self, angle):
        self.rotation[2] += angle
        self.rotation[2] = self.rotation[2] % math.tau

    def loadJson(self, mesh):
        object = open("Minecraft/"+mesh)
        data = json.load(object)

        self.vertices = data['vertices']
        self.faces = data['faces']

        self.triangles = []

        # Create Triangles
        for face in self.faces:
            if len(face) == 3:
                self.triangles.append(face)
            if len(face) > 3:
                # This is called Fan Triangulation
                for i in range(len(face)-2):
                    new_triangle = [ face[0], face[i+1], face[i+2]]
                    self.triangles.append(new_triangle)
        
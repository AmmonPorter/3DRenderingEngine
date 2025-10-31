import math
import json
import struct

class mesh:
    def __init__(self, mesh):
        if ".json" in mesh:
            self.loadJson(mesh)
        if ".stl" in mesh:
            self.loadSTL(mesh)



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

    def loadSTL(self, mesh):
        self.vertices = []
        self.faces = []
        self.triangles = []
        print(f"Loading BINARY STL file: {mesh}")
        
        # This dictionary will store {vertex_tuple: index}
        vertex_lookup = {}

        try:
            with open("Minecraft/"+mesh, 'rb') as file:
                # 1. Skip the 80-byte header
                header = file.read(80)

                # 2. Read the 4-byte triangle count
                count_bytes = file.read(4)
                # Unpack it as a 4-byte unsigned integer ('<I')
                triangle_count = struct.unpack('<I', count_bytes)[0]

                print(f"File contains {triangle_count} triangles.")

                # 3. Loop for each triangle
                for _ in range(triangle_count):
                    # Read the 50-byte chunk for this triangle
                    # Format: 12 floats (Normal, V1, V2, V3) + 2 attribute bytes
                    # '<12fH' = 12 4-byte floats, 1 2-byte short
                    try:
                        data = file.read(50)
                        if len(data) < 50:
                            break # Reached end of file unexpectedly

                        # Unpack the 12 floats and 1 short
                        unpacked_data = struct.unpack('<12fH', data)

                        # We only care about the vertices, which are
                        # floats at indices 3-11
                        v1 = (unpacked_data[3], unpacked_data[4], unpacked_data[5])
                        v2 = (unpacked_data[6], unpacked_data[7], unpacked_data[8])
                        v3 = (unpacked_data[9], unpacked_data[10], unpacked_data[11])
                        
                        current_triangle_indices = []
                        
                        # --- Run "Vertex Welding" for each vertex ---
                        for v in [v1, v2, v3]:
                            if v not in vertex_lookup:
                                # New vertex
                                self.vertices.append(v)
                                vertex_lookup[v] = len(self.vertices) - 1
                            
                            # Add the index to our triangle
                            current_triangle_indices.append(vertex_lookup[v])
                        
                        # Add the completed triangle to the main list
                        self.triangles.append(current_triangle_indices)

                    except struct.error as e:
                        print(f"Error unpacking triangle data: {e}")
                        break

            print(f"Loaded {len(self.vertices)} unique vertices and {len(self.triangles)} triangles.")

        except FileNotFoundError:
            print(f"ERROR: Could not find STL file at {mesh}")
            raise
        except Exception as e:
            print(f"ERROR: Failed to parse STL file {mesh}. Error: {e}")
            raise
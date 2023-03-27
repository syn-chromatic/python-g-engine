from components.shared_dcs import Polygons, Triangles, Quads
from components.vertices import MeshConverter
from pathlib import Path


class OBJModelFormat:
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def get_model_triangles(self) -> list[Polygons]:
        vertices, faces = [], []
        with open(self.file_path) as f:
            for line in f:
                tokens = line.split()
                if not tokens:
                    continue

                if tokens[0] == "v":
                    vertex = tuple(float(i) for i in tokens[1:4])
                    vertices.append(vertex)
                elif tokens[0] == "f":
                    face_indices = [int(tok.split("/")[0]) - 1 for tok in tokens[1:]]
                    if len(face_indices) == 3:
                        faces.append(tuple(face_indices))

        triangles = Triangles(vertices, faces)
        polygons = [Polygons(triangles)]
        return polygons

    def get_model_quads(self) -> list[Polygons]:
        vertices, faces = [], []
        with open(self.file_path) as f:
            for line in f:
                tokens = line.split()
                if not tokens:
                    continue

                if tokens[0] == "v":
                    vertex = tuple(float(i) for i in tokens[1:4])
                    vertices.append(vertex)
                elif tokens[0] == "f":
                    face_indices = [int(tok.split("/")[0]) - 1 for tok in tokens[1:]]
                    if len(face_indices) == 4:
                        faces.append(tuple(face_indices))

        quads = Quads(vertices, faces)
        polygons = [Polygons(quads)]
        return polygons

    def get_polygons(self) -> list[Polygons]:
        mesh1 = self.get_model_triangles()
        mesh2 = self.get_model_quads()
        mesh2 = MeshConverter(mesh2).quads_to_triangles()
        polygons = [*mesh1, *mesh2]
        return polygons

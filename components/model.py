from components.shared_dcs import Polygons, Triangles, Quads

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

    def quads_to_triangles(self, polygons: list[Polygons]) -> list[Polygons]:

        for idx, polys in enumerate(polygons):
            polys_type = polys.type

            if isinstance(polys_type, Quads):
                triangle_faces: list[tuple[int, int, int]] = []
                quad_faces = polys_type.faces
                for quad in quad_faces:
                    triangle1 = (quad[0], quad[1], quad[2])
                    triangle2 = (quad[0], quad[2], quad[3])

                    triangle_faces.extend([triangle1, triangle2])
                triangles = Triangles(polys_type.vertices, triangle_faces)
                polygons[idx].type = triangles

        return polygons

    def get_polygons(self) -> list[Polygons]:
        triangles = self.get_model_triangles()
        quads = self.get_model_quads()
        quads_to_triangles = self.quads_to_triangles(quads)

        polygons = [*triangles, *quads_to_triangles]
        return polygons

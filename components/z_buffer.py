from components.vectors import Vector3D
from components.polygons import Triangle, Quad


from typing import Union


class ZBufferSort1:
    def __init__(self, camera_position: Vector3D):
        self.camera_position = camera_position

    def get_centroid(self, polygon: Union[Triangle, Quad]):
        vertices_sum = Vector3D(0, 0, 0)
        num_vertices = len(polygon.vertices)

        for vertex in polygon.vertices:
            vertices_sum = vertices_sum.add_vector(vertex)

        return vertices_sum.divide(num_vertices)

    def get_sorted_polygons(
        self, polygons: list[Union[Triangle, Quad]]
    ) -> list[Union[Triangle, Quad]]:
        camera_position = self.camera_position
        return sorted(
            polygons,
            key=lambda p: camera_position.get_distance(self.get_centroid(p)),
            reverse=True,
        )


class ZBufferSort2:
    def __init__(self, camera_position):
        self.camera_position = camera_position

    def get_centroid(self, polygon):
        vertices = polygon.vertices
        num_vertices = len(vertices)
        vertices_sum = Vector3D(0.0, 0.0, 0.0)

        for vertex in vertices:
            vertices_sum = vertices_sum.add_vector(vertex)

        return vertices_sum.divide(num_vertices)

    def get_centroid_distance(self, polygon):
        centroid = self.get_centroid(polygon)
        distance = self.camera_position.get_distance(centroid)
        return distance

    def get_polygon_max_z(self, polygon):
        if isinstance(polygon, Triangle):
            vertices = polygon.vertices
        elif isinstance(polygon, Quad):
            vertices = polygon.vertices
        else:
            raise TypeError("Invalid polygon type")

        max_z = float("-inf")

        for vertex in vertices:
            distance = self.camera_position.get_distance(vertex)

            if distance > max_z:
                max_z = distance

        return max_z

    def merge_sort(self, distances, left, right):
        if left < right:
            mid = left + (right - left) // 2
            self.merge_sort(distances, left, mid)
            self.merge_sort(distances, mid + 1, right)
            self.merge(distances, left, mid, right)

    def merge(self, distances, left, mid, right):
        n1 = mid - left + 1
        n2 = right - mid

        left_distances = distances[left : (left + n1)]
        right_distances = distances[(mid + 1) : (mid + 1 + n2)]

        i = j = 0
        k = left

        while i < n1 and j < n2:
            if left_distances[i][0] > right_distances[j][0]:
                distances[k] = left_distances[i]
                i += 1
            else:
                distances[k] = right_distances[j]
                j += 1
            k += 1

        while i < n1:
            distances[k] = left_distances[i]
            i += 1
            k += 1

        while j < n2:
            distances[k] = right_distances[j]
            j += 1
            k += 1

    def get_sorted_polygons(self, polygons):
        distances = [
            (self.get_centroid_distance(polygons[i]), i) for i in range(len(polygons))
        ]

        self.merge_sort(distances, 0, len(polygons) - 1)
        sorted_polygons = [polygons[index] for _, index in distances]
        return sorted_polygons

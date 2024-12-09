import re
from typing import List
import numpy as np

from PolygonADT import Polygon, Coord


def get_edges_and_angles(polygon):

    edges = []
    angles = []

    for coord in range(len(polygon.vertices) - 1):
        c1 = (polygon.vertices[coord].x, polygon.vertices[coord].y)
        c2 = (polygon.vertices[coord + 1].x, polygon.vertices[coord + 1].y)

        edge_length = np.linalg.norm(np.array(c1) - np.array(c2))
        edges.append(edge_length)

        angle = np.degrees(np.arctan2(c2[1] - c1[1], c2[0] - c1[0]))
        angles.append(angle)

    return edges, angles


def main():
    polygons: List[Polygon] = []
    test_poly = []

    with open('../Milestone_Input/Milestone 2/Source.txt', 'r') as input_file:

        for line in input_file:
            line = line.strip()

            if re.match('^boundary', line):
                polygon = Polygon()

                line = input_file.readline().strip()
                polygon.layer = int(line.split(' ')[1])

                line = input_file.readline().strip()
                polygon.datatype = int(line.split(' ')[1])

                line = input_file.readline().strip()
                line = re.sub(r'\s+', ' ', line)
                xy = line.split(' ')[1:]

                polygon.V = int(xy[0])

                for i in range(1, len(xy), 2):
                    x = int(xy[i])
                    y = int(xy[i + 1])
                    polygon.vertices.append(Coord(x, y))

                if polygon:
                    polygons.append(polygon)

    with open('../Milestone_Input/Milestone 2/POI.txt', 'r') as input_file:

        for line in input_file:
            line = line.strip()

            if re.match('^boundary', line):
                polygon = Polygon()

                line = input_file.readline().strip()
                polygon.layer = int(line.split(' ')[1])

                line = input_file.readline().strip()
                polygon.datatype = int(line.split(' ')[1])

                line = input_file.readline().strip()
                line = re.sub(r'\s+', ' ', line)
                xy = line.split(' ')[1:]

                polygon.V = int(xy[0])

                for i in range(1, len(xy), 2):
                    x = int(xy[i])
                    y = int(xy[i + 1])
                    polygon.vertices.append(Coord(x, y))

                if polygon:
                    test_poly.append(polygon)

    test_edges, test_angles = get_edges_and_angles(test_poly[0])

    with open('../Milestone_Output/Milestone 2/output.txt', 'w') as output_file:

        for polygon in polygons:
            poly_edges, poly_angles = get_edges_and_angles(polygon)

            if len(poly_edges) == len(test_edges) and len(poly_angles) == len(test_angles):
                if np.allclose(poly_edges, test_edges) and np.allclose(poly_angles, test_angles):
                    output_file.write(f'boundary\r')
                    output_file.write(f'layer {polygon.layer}\r')
                    output_file.write(f'datatype {polygon.datatype}\r')

                    s = f"xy  {polygon.V}  " + '  '.join(f"{c.x} {c.y}" for c in polygon.vertices)
                    output_file.write(s + '\r')

                    output_file.write('endel\r')

    return


if __name__ == '__main__':
    main()

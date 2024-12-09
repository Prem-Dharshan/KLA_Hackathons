import re
import numpy as np
from typing import List
from PolygonADT import Polygon, Coord


# Normalize the polygon orientation (clockwise or counter-clockwise)
def normalize_polygon(polygon):
    """
    Normalize the polygon vertices by sorting them in counter-clockwise order
    relative to the centroid.
    """
    # Compute the centroid of the polygon
    centroid_x = sum(c.x for c in polygon.vertices) / len(polygon.vertices)
    centroid_y = sum(c.y for c in polygon.vertices) / len(polygon.vertices)

    # Sort vertices based on the angle with respect to the centroid (to ensure consistent orientation)
    def angle_from_centroid(c):
        return np.arctan2(c.y - centroid_y, c.x - centroid_x)

    polygon.vertices.sort(key=angle_from_centroid)


def get_centroid(polygon):
    """
    Function to calculate the centroid of the polygon.
    """
    n = len(polygon.vertices)
    centroid_x = sum(c.x for c in polygon.vertices) / n
    centroid_y = sum(c.y for c in polygon.vertices) / n
    return Coord(centroid_x, centroid_y)


def get_angle_edge_pairs(polygon):
    """
    Function to calculate the edge length and the angle for each edge of the polygon.
    """
    edges = []
    angles = []

    centroid = get_centroid(polygon)

    for i in range(len(polygon.vertices) - 1):
        # Get the coordinates of two consecutive vertices
        c1 = polygon.vertices[i]
        c2 = polygon.vertices[i + 1]

        # Edge length: Distance between consecutive vertices
        edge_length = np.linalg.norm(np.array([c2.x, c2.y]) - np.array([c1.x, c1.y]))
        edges.append(edge_length)

        # Angle: Calculate the angle between the centroid and the vertex
        angle = np.degrees(np.arctan2(c2.y - centroid.y, c2.x - centroid.x))
        angles.append(angle)

    # Also calculate for the edge between the last vertex and the first vertex (closing the polygon)
    c1 = polygon.vertices[-1]
    c2 = polygon.vertices[0]
    edge_length = np.linalg.norm(np.array([c2.x, c2.y]) - np.array([c1.x, c1.y]))
    edges.append(edge_length)

    angle = np.degrees(np.arctan2(c2.y - centroid.y, c2.x - centroid.x))
    angles.append(angle)

    return edges, angles


def main():
    polygons: List[Polygon] = []
    test_poly = []

    # Read polygons from Source.txt
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

    # Read test polygon from POI.txt
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

    # Normalize the test polygon to ensure consistent orientation
    normalize_polygon(test_poly[0])
    test_edges, test_angles = get_angle_edge_pairs(test_poly[0])

    # Write matching polygons to output.txt
    with open('../Milestone_Output/Milestone 2/output.txt', 'w') as output_file:
        for polygon in polygons:
            # Normalize each polygon to ensure consistent orientation
            normalize_polygon(polygon)

            poly_edges, poly_angles = get_angle_edge_pairs(polygon)

            # Relax the precision tolerance slightly for comparison
            if len(poly_edges) == len(test_edges) and len(poly_angles) == len(test_angles):
                if np.allclose(poly_edges, test_edges, atol=1e-5, rtol=1e-5) and np.allclose(poly_angles, test_angles,
                                                                                             atol=1e-5, rtol=1e-5):
                    output_file.write(f'boundary\r')
                    output_file.write(f'layer {polygon.layer}\r')
                    output_file.write(f'datatype {polygon.datatype}\r')

                    s = f"xy  {polygon.V}  " + '  '.join(f"{c.x} {c.y}" for c in polygon.vertices)
                    output_file.write(s + '\r')

                    output_file.write('endel\r')

    return


if __name__ == '__main__':
    main()

# Credits: https://github.com/MrRhuezzler/
# https://github.com/MrRhuezzler/kla-hackathon-23/blob/master/main.py

from typing import *
import numpy as np
import cv2 as cv
import threading
import matplotlib.pyplot as plt

MILESTONE = 7


class Boundary:
    def __init__(self, layer, datatype, xy) -> None:
        self.layer = Boundary.parseLayer(layer)
        self.datatype = Boundary.parseDatatype(datatype)
        self.xy_string = xy
        self.xy = Boundary.parsePoints(xy)

    def __hash__(self) -> int:
        return hash(self.xy_string)

    @staticmethod
    def parseDatatype(datatype):
        return int(datatype.split(" ")[1])

    @staticmethod
    def parseLayer(layer):
        return int(layer.split(" ")[1])

    @staticmethod
    def parsePoints(xy):
        return list(tuple(map(int, x.split(" "))) for x in xy.split("  ")[2:])

    @staticmethod
    def findAngle(a, b, c):
        ba = a - b
        bc = c - b
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)
        return np.degrees(angle)

    @staticmethod
    def findDistance(a, b):
        return np.linalg.norm(a - b)

    def comparePolygons(p1, p2):
        p1 = p1.xy + [p1.xy[1]]
        p2 = p2.xy + [p2.xy[1]]

        if len(p1) == len(p2):
            for i in range(2, len(p1)):
                a1 = Boundary.findAngle(np.array(p1[i]), np.array(p1[i - 1]), np.array(p1[i - 2]))
                a2 = Boundary.findAngle(np.array(p2[i]), np.array(p2[i - 1]), np.array(p2[i - 2]))

                if np.abs(a1 - a2) > 1e-2:
                    return False

            side_length_1 = []
            side_length_2 = []

            for i in range(1, len(p1)):
                side_length_1.append(Boundary.findDistance(np.array(p1[::-1][i]), np.array(p1[::-1][i - 1])))
                side_length_2.append(Boundary.findDistance(np.array(p2[::-1][i]), np.array(p2[::-1][i - 1])))

            ratios1 = [side_length_1[i] / side_length_1[i - 1] for i in range(1, len(side_length_1))]
            ratios2 = [side_length_2[i] / side_length_2[i - 1] for i in range(1, len(side_length_2))]

            for r1, r2 in zip(ratios1, ratios2):
                print(abs(r1 - r2))
                if abs(r1 - r2) > 3.5:
                    return False

            return True
        else:
            False

    def formattedPrint(self):
        string = "boundary\n"
        string += f"layer {self.layer}\n"
        string += f"datatype {self.datatype}\n"
        string += f"xy {len(self.xy)} "
        for point in self.xy:
            string += f"{point[0]} {point[1]} "

        string = string[:-1] + "\n"
        string += "endel"
        return string

    def __str__(self) -> str:
        return f"{self.layer} | {self.datatype} | {self.xy}"


def parseInput(lines):
    boundaries = []
    insideBoundary = False
    data = {}

    isHeader = True

    headerData = ""
    for index, line in enumerate(lines):
        line = line.strip()

        if "boundary" in line:
            insideBoundary = True
            isHeader = False

        if isHeader:
            headerData += line + "\n"

        if insideBoundary:
            if "layer" in line:
                data["layer"] = line
            elif "datatype" in line:
                data["datatype"] = line
            elif "xy" in line:
                data["xy"] = line
            elif "endel" in line:
                boundaries.append(Boundary(**data))
                data = {}
                insideBoundary = False

    return {
        "header": headerData,
        "boundaries": boundaries
    }


def writeOutput(data):
    with open(f"../Milestone_Output/{MILESTONE}.txt", "w") as file:
        file.write(data + "\nendstr\nendlib\n")


def formImage(polys):
    figure, axis = plt.subplots()
    for poly in polys:
        axis.fill(list(p[0] for p in poly), list(p[1] for p in poly), color="black")
    axis.set_axis_off()

    figure.canvas.draw()

    img = np.frombuffer(figure.canvas.tostring_rgb(), dtype=np.uint8)
    img = img.reshape(figure.canvas.get_width_height()[::-1] + (3,))
    img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
    return img


# def split(a, n):
#     k, m = divmod(len(a), n)
#     return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

# Tried threading
# def matcher(source, poi, addToOutput):
#     template = formImage([f.xy for f in poi])
#     for s in source:
#         source = formImage([s.xy])
#         res = cv.matchTemplate(source, template, cv.TM_CCOEFF_NORMED)
#         min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
#         if max_val > 0.7:
#             print(s.formattedPrint())
#             addToOutput(s)
#             # break

def matchSpliter(source: List[Boundary], poi: List[Boundary]):
    matches = set()
    if len(poi) <= 1:
        for p in poi:
            for s in source:
                if len(p.xy) == len(s.xy):
                    match = cv.matchShapes(np.array(p.xy, dtype=np.int32), np.array(s.xy, dtype=np.int32), 2, 0.0)
                    if match < 1e-2:
                        matches.add(s)

        return matches
    else:
        # for p in poi:
        #     template = formImage([p.xy])
        #     for s in source:
        #         source = formImage([s.xy])
        #         res = cv.matchTemplate(source, template, cv.TM_CCOEFF_NORMED)
        #         min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

        #         print(max_val)
        #         if max_val > 0.7:
        #             matches.add(s)
        #             # break

        # return matches
        for p in poi:
            for s in source:
                if len(p.xy) == len(s.xy):
                    match = cv.matchShapes(np.array(p.xy, dtype=np.int32), np.array(s.xy, dtype=np.int32), 2, 0.0)
                    if match < 1e-8:
                        matches.add(s)

        return matches


if __name__ == "__main__":
    with open(f'../Milestone_Input/Milestone {MILESTONE}/source.txt') as source:
        with open(f'../Milestone_Input/Milestone {MILESTONE}/POI.txt') as poi:
            source = parseInput(source.readlines())
            poi = parseInput(poi.readlines())

            matches = matchSpliter(source["boundaries"], poi["boundaries"])

            print(len(matches))

            data_to_write = source["header"]
            for match in matches:
                data_to_write += match.formattedPrint() + "\n"
            writeOutput(data_to_write)

# Given a set of source polygons and target polygons, each boundary is a set of (x,y) coordinates, find the source bounaries and target polygons, each polygon is a set of (x,y) coordinates, find the source polygons that match with all of the target polygons, the polygons are to be matched with
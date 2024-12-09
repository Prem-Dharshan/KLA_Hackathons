import os
import numpy as np
from custom_logging import setup_logger

# Setup the logger
logger = setup_logger()


class Wafer:
    def __init__(self, dia=None, npts=None, angle=None):
        self.dia = dia
        self.nPts = npts
        self.angle = angle

    def __str__(self):
        return f"Wafer:\n\tDia: {self.dia}\n\tNpts: {self.nPts}\n\tAngle: {self.angle}"


def process_wafer(input_file, output_file):
    wafer = Wafer()

    try:
        logger.info(f"Attempting to read the input file {input_file}...")
        with open(input_file) as f:
            for line in f.readlines():
                if "WaferDiameter" in line:
                    wafer.dia = int(line.split(':')[1])
                elif "NumberOfPoints" in line:
                    wafer.nPts = int(line.split(':')[1])
                elif "Angle" in line:
                    wafer.angle = int(line.split(':')[1])
                else:
                    continue
        logger.success(f"Successfully parsed the input file {input_file}.")
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return
    except Exception as e:
        logger.error(f"Unexpected error while parsing the input file: {e}")
        return

    logger.info(f"Parsed wafer details:\n{wafer}")

    # Prepare points
    x1, y1 = -wafer.dia // 2, 0
    x2, y2 = wafer.dia // 2, 0

    try:
        logger.info("Generating points using linspace...")
        pts = np.linspace(x1, x2, wafer.nPts)
        pts = np.round(pts, 4).astype(float)
        logger.debug(f"Generated points: {pts}")

        logger.info("Applying rotation transformation...")
        theta = np.radians(wafer.angle)

        x_rotated = pts * np.cos(theta)
        y_rotated = pts * np.sin(theta)

        x_rotated = np.round(x_rotated, 4).astype(float)
        y_rotated = np.round(y_rotated, 4).astype(float)

        x_rotated = np.where(np.isclose(x_rotated, 0), 0.0, x_rotated)
        y_rotated = np.where(np.isclose(y_rotated, 0), 0.0, y_rotated)

        rotated_points = np.column_stack((x_rotated, y_rotated))

        # Apply lexsort for sorting the rotated points
        logger.info("Sorting rotated points using lexsort...")
        sorted_indices = np.lexsort((rotated_points[:, 1], rotated_points[:, 0]))
        rotated_points_sorted = rotated_points[sorted_indices]

        rotated_points_list = rotated_points_sorted.tolist()
        rotated_points_tuples = [tuple(point) for point in rotated_points_list]

        logger.success(f"Successfully computed rotated and sorted points for {input_file}.")
    except Exception as e:
        logger.error(f"Error during point generation or rotation: {e}")
        return

    # Writing the rotated points to the output file
    try:
        logger.info(f"Writing rotated points to output file {output_file}...")
        with open(output_file, "w") as f:
            for point in rotated_points_tuples:
                f.write(f"({point[0]},{point[1]})\n")
        logger.success(f"Successfully wrote rotated points to the output file {output_file}.")
    except IOError as e:
        logger.error(f"Error writing to output file: {e}")
        return
    except Exception as e:
        logger.error(f"Unexpected error during file writing: {e}")
        return


def main():
    input_dir = "../MilestoneInput/01"  # Directory containing input files
    output_dir = "../MilestoneOutput/01"  # Directory for the output files

    # List all .txt files in the input directory
    input_files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]

    # Process each input file
    for input_file in input_files:
        input_file_path = os.path.join(input_dir, input_file)
        output_file_path = os.path.join(output_dir, f"TC{input_file.split('.')[0]}.txt")

        process_wafer(input_file_path, output_file_path)


if __name__ == "__main__":
    main()

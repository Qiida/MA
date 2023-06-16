from pathlib import Path
from os.path import join

ROOT_DIR = Path(__file__).parent.parent.parent
LIDAR_DIR = join(ROOT_DIR, "resources", "lidar")
CAM_DIR = join(ROOT_DIR, "resources", "camera")
SVG_DIR = join(ROOT_DIR, "resources", "svg")
CALIBRATION_DIR = join(ROOT_DIR, "resources", "calibration")
PROJECTS_DIR = join(ROOT_DIR, "projects")
RESOURCES_DIR = join(ROOT_DIR, "resources")
ANALYSIS_DIR = join(ROOT_DIR, "analysis")


if __name__ == '__main__':
    print(ROOT_DIR)
    print(LIDAR_DIR)
    print(CAM_DIR)
    print(SVG_DIR)
    print(CALIBRATION_DIR)
    print(PROJECTS_DIR)
    print(RESOURCES_DIR)
    print(ANALYSIS_DIR)

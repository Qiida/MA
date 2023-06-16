from os.path import join
import matplotlib
from matplotlib import pyplot as plt

from src.app.plot.setAxis import set_axis
from src.data.TestVehicle import TestVehicle
from src.utils import readMatFile
from src.data.preparation.filterNanColumns import filterNanColumns
from src.lcm.LidarCameraMapper import LidarCameraMapper
from src.utils import LIDAR_DIR, CAM_DIR

matplotlib.use("TkAgg")


def plot(i):
    fig = plt.figure()
    axL = fig.add_subplot(121, projection="3d")
    set_axis(axis=axL)
    axR = fig.add_subplot(122)
    axR.imshow(frames[i].image)
    # lidarObject.plotIdNr(axL, images[i].idNr)
    lcMapper.plotLidarObjects(frames[i].idNr, axL)
    lcMapper.testVehicle.boundingBox.draw(axL)
    fig.suptitle('Time: {} s'.format(frames[i].time))
    fig.canvas.draw_idle()
    plt.show()


if __name__ == '__main__':
    data = readMatFile(join(LIDAR_DIR, "Export_pp_20191125_IM_1_split_053.mat"))["data"]
    filterNanColumns(data)

    lcMapper = LidarCameraMapper(testVehicle=TestVehicle("TEASY3"),
                                 matFile=join(LIDAR_DIR, "Export_pp_20191125_IM_1_split_053.mat"),
                                 camFile=join(CAM_DIR, "20191125_IM_1_split_053_front.avi"))

    lidarObject = lcMapper.lidarObjects[13]
    frames = lcMapper.buildFrames()
    plot(0)
    print("wow")

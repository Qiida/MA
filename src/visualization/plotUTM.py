import matplotlib

from os.path import join
from matplotlib import pyplot

from src.utils import ROOT_DIR
from src.data.preparation.computeUTM import computeUTM_ego_obj
from src.utils import readMatFile
from src.data.TestVehicle import TestVehicle

matplotlib.use("TkAgg")


def plotUTM(ego):

    pyplot.plot(ego.x, ego.y, linewidth=2, color="black")
    pyplot.grid("on")
    pyplot.show()


if __name__ == '__main__':
    path = join(ROOT_DIR, 'resources', 'lidar', 'Export_pp_20191125_IM_1_split_050.mat')
    matFile = readMatFile(path)
    ego, obj = computeUTM_ego_obj(data=matFile['data'], testVehicle=TestVehicle("TEASY3"))

    plotUTM(ego=ego)

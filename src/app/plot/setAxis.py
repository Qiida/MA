from matplotlib import pyplot as plt


def set_axis(axis):
    # axis.axis("equal")
    axis.axis("auto")
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.set_xlim([-15, 15])
    axis.set_ylim([-15, 15])
    axis.set_zlim([-15, 15])
    axis.azim = -180
    axis.elev = 90
    # plt.axis('off')

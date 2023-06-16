def plotBox(ax, u, v, c, lineWidth=3):
    ax.plot((u[0], u[0]), (v[0], v[1]), c=c, linewidth=lineWidth)
    ax.plot((u[0], u[1]), (v[1], v[1]), c=c, linewidth=lineWidth)
    ax.plot((u[1], u[1]), (v[1], v[0]), c=c, linewidth=lineWidth)
    ax.plot((u[1], u[0]), (v[0], v[0]), c=c, linewidth=lineWidth)

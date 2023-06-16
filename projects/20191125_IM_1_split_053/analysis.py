import os.path

import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use("TkAgg")

SEED = 214
N = 111

overviewDF = pd.read_csv(os.path.join("csv", "overview.csv"))
path = os.path.join("csv", f"projection_s{SEED}_n{N}.csv")
df = pd.read_csv(path)

print("The End.")

distance_mean = []
numberOfPoints = []
for i, row in overviewDF.iterrows():
    distance_mean.append(row.distance_mean)
    numberOfPoints.append(row.numberOfPoints)

data = {}

for n in range(10, 500):
    data.update(
        {
            n: []
        }
    )

for i, n in enumerate(numberOfPoints):
    data.get(n).append(distance_mean[i])

# tabel = pd.DataFrame(data)
figure, axis = plt.subplots(1, 1, layout="constrained")
# axis.scatter(numberOfPoints, distance_mean)
#

#
# figure.savefig(
#     f"Random_Gesamtauswertung.pdf",
#     format="pdf", bbox_inches="tight"
# )
# plt.show()
dataSample = [data.get(10), data.get(20), data.get(30), data.get(40), data.get(50), data.get(100), data.get(200), data.get(300), data.get(400), data.get(499)]

xTicks = [10, 20, 30, 40, 50, 100, 200, 300, 400, 499]
axis.boxplot(dataSample, showfliers=False, whis=0.5)


# axis.set_xticks(xTicks)
axis.set_xticklabels(xTicks)
axis.set_xlabel("Anzahl der Punkte [-]")
axis.set_ylabel("Durchschnittliche Abweichung [px]")
plt.title("Durchschnittliche Projektionsfehler")
# axis.set_xlim([490, 500])
# axis.set_ylim([-10, 60000])
figure.savefig(
   "boxplot.pdf",
    format="pdf", bbox_inches="tight"
)

# overviewDF.boxplot()
# plt.show()

import os
from os.path import join

from src.utils.directories import ROOT_DIR


i = 0

path = join(ROOT_DIR, "output", "images")

for filename in os.listdir(path):
    dest = "f_{}.png".format(i)
    src = join(path, filename)
    dest = join(path, dest)
    os.rename(src, dest)
    i += 1


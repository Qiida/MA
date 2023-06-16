import numpy as np

cameraParams = np.load("CameraParams.npz")
intrinsic = cameraParams.get("cameraMatrix")

print("stop")
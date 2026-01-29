import numpy as np
import matplotlib.pyplot as plt

angles = np.load("angle_log.npy")
angles = (angles[688:] / 360) * 2 * np.pi

step = 0.01
t = np.arange(0, len(angles)*step, step)

plt.plot(t, angles)
plt.grid()
plt.show()
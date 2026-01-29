import numpy as np
import matplotlib.pyplot as plt

angles = np.load("angle_log.npy")
angles = (angles[688:] / 360) * 2 * np.pi

plt.plot(angles)
plt.grid()
plt.show()
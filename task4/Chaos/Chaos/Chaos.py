
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation

la, si, b = 28, 10, 8/3
dt = 0.01
N = 10000
delta=1e-4

x1, y1, z1 = np.zeros(N), np.zeros(N), np.zeros(N)
x1[0], y1[0], z1[0] = 1, 1, 1

x2, y2, z2 = np.zeros(N), np.zeros(N), np.zeros(N)
x2[0], y2[0], z2[0] = 1+delta, 1+delta, 1+delta 

def lorenz(x, y, z, la, si, b, dt):
    dx = si * (y - x)
    dy = x * (la - z) - y
    dz = x * y - b * z
    return x + dx * dt, y + dy * dt, z + dz * dt

for i in range(1, N):
    x1[i], y1[i], z1[i] = lorenz(x1[i-1], y1[i-1], z1[i-1], la, si, b, dt)
    x2[i], y2[i], z2[i] = lorenz(x2[i-1], y2[i-1], z2[i-1], la, si, b, dt)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

frames = []
for i in range(1, N, 10): 
    line1, = ax.plot(x1[:i], y1[:i], z1[:i], color='blue', lw=0.5)
    line2, = ax.plot(x2[:i], y2[:i], z2[:i], color='red', lw=0.5)
    frames.append([line1, line2])

animation = ArtistAnimation(fig, frames, interval=10, blit=True)
plt.show()




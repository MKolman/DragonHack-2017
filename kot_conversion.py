#import matplotlib.pyplot as plt
import numpy as np

def convert(deg, r=100):
    if 0 <= deg <= 90:
        left = np.cos(2*deg/360*2*np.pi)*100
        right = -100
    elif 90 < deg <= 180:
        left = -100
        right = -np.cos(2*(deg-90)/360*2*np.pi)*100
    elif 180 < deg <= 270:
        left = -np.cos(2*(deg-180)/360*2*np.pi)*100
        right = 100
    elif 270 < deg <= 360:
        left = 100
        right = np.cos(2*(deg-270)/360*2*np.pi)*100
    else:
        print('Should not be here')
        left = 0
        right = 0
    return left/100*r, right/100*r


"""
r = np.arange(0, 1, 0.01)
theta = 2 * np.pi * r
deg = theta/2/np.pi*360
left, right = np.array(list(map(convert, deg))).T
left += 200
right += 200

ax = plt.subplot(111, projection='polar')
ax.plot(-theta, left, label='left')
ax.plot(-theta, right, label='right')
ax.set_rlim(0, 310)
plt.legend()
#ax.set_rmax(2)
#ax.set_rticks([0.5, 1, 1.5, 2])  # less radial ticks
#ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
ax.grid(True)

plt.show()
"""

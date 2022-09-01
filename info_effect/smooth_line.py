import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline


# plot double lines
def plot_smooth_lines(n, x, y, pic_name):
    # initialize plot parameters
    print('picture name: %s, len of data: %d' % (pic_name, n))
    plt.rcParams['figure.figsize'] = (10 * 16 / 9, 10)
    plt.subplots_adjust(left=0.06, right=0.94, top=0.92, bottom=0.08)

    # 对x和y1进行插值
    x_smooth = np.linspace(x.min(), x.max(), 50)
    y1_smooth = make_interp_spline(x, y)(x_smooth)
    # plot curve 1
    plt.plot(x_smooth, y1_smooth, label='Score')

    # show the legend
    plt.legend()

    # show the picture
    plt.show()

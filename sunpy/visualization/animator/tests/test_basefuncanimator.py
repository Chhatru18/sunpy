
from functools import partial

import matplotlib.animation as mplanim
import matplotlib.pyplot as plt
import numpy as np
import pytest

from sunpy.visualization.animator import BaseFuncAnimator


class FuncAnimatorTest(BaseFuncAnimator):
    def plot_start_image(self, ax):
        im = ax.imshow(self.data[0])
        if self.if_colorbar:
            self._add_colorbar(im)
        return im


def update_plotval(val, im, slider, data):
    i = int(val)
    im.set_array(data[i])


def button_func1(*args, **kwargs):
    print(*args, **kwargs)


@pytest.mark.parametrize('fig, colorbar, buttons', ((None, False, [[], []]),
                                                    (plt.figure(), True, [[button_func1], ["hi"]])))
def test_base_func_init(fig, colorbar, buttons):
    data = np.random.random((3, 10, 10))
    func = partial(update_plotval, data=data)
    funcs = [func]
    ranges = [(0, 3)]

    tfa = FuncAnimatorTest(data, funcs, ranges, fig=fig, colorbar=colorbar,
                           button_func=buttons[0],
                           button_labels=buttons[1])

    tfa.label_slider(0, "hello")


@pytest.fixture
def funcanimator():
    data = np.random.random((3, 10, 10))
    func = partial(update_plotval, data=data)
    funcs = [func]
    ranges = [(0, 3)]

    return FuncAnimatorTest(data, funcs, ranges)


def test_to_anim(funcanimator):
    ani = funcanimator.get_animation()
    assert isinstance(ani, mplanim.FuncAnimation)

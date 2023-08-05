from typing import Optional, Union

from matplotlib.axes import Axes
from pandas import Series, DataFrame

from mpl_format.axes import AxesFormatter


class BarPlot(object):

    def __init__(self, data: Union[Series, DataFrame],
                 ax: Optional[Union[Axes, AxesFormatter]] = None):

        self._data: Union[Series, DataFrame] = data
        if ax is None:
            self._axf = AxesFormatter()
        elif isinstance(ax, Axes):
            self._axf = AxesFormatter(axes=ax)
        elif isinstance(ax, AxesFormatter):
            self._axf = ax
        else:
            raise TypeError('ax must be None, Axes or AxesFormatter')

    def plot_v_bars(
            self,
            x: Optional[str] = None,
            labels: Optional[str] = None,
            y_top: Optional[str] = None,
            width: float = 0.8,
            y_bottom: float = 0.0,
            h_align: str = 'center'
    ) -> 'BarPlot':

        if isinstance(self._data, Series):
            # add bars
            for c, (category, value) in enumerate(self._data.items()):
                if isinstance(category, str):
                    x_center = c + 1
                else:
                    x_center = category
                self._axf.add_rectangle(
                    width=width, height=value,
                    x_center=x_center,
                    y_bottom=y_bottom
                )
        else:  # DataFrame
            pass

        return self

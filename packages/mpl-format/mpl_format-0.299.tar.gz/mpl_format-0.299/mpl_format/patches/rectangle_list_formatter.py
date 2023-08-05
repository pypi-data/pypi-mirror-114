from typing import List, Union

from matplotlib.patches import Rectangle

from mpl_format.patches import PatchListFormatter


class RectangleListFormatter(PatchListFormatter):

    _patches: List[Rectangle]

    def __init__(self, patches: List[Rectangle]):

        super().__init__(patches)

    @property
    def heights(self) -> List[Union[int, float]]:

        return [r.get_height() for r in self._patches]

    @property
    def widths(self) -> List[Union[int, float]]:

        return [r.get_width() for r in self._patches]

    @property
    def x_lefts(self) -> List[Union[int, float]]:

        return [r.get_x() for r in self._patches]

    @property
    def y_bottoms(self) -> List[Union[int, float]]:
        return [r.get_y() for r in self._patches]

    @property
    def x_rights(self) -> List[Union[int, float]]:

        return [r.get_x() + r.get_width() for r in self._patches]

    @property
    def y_tops(self) -> List[Union[int, float]]:

        return [r.get_y() + r.get_height() for r in self._patches]

    @property
    def x_centers(self) -> List[Union[int, float]]:

        return [r.get_x() + r.get_width() / 2 for r in self._patches]

    @property
    def y_centers(self) -> List[Union[int, float]]:

        return [r.get_y() + r.get_height() / 2 for r in self._patches]

    @property
    def angles(self) -> List[Union[int, float]]:

        return [r.angle for r in self._patches]

"""Path data class implementation for the svg's
`continual 3D bezier curve` (S).
"""

from typing import Union

from apysc._converter.to_apysc_val_from_builtin import \
    get_copied_int_from_builtin_val
from apysc._geom.path_data_base import PathDataBase
from apysc._type.int import Int


class PathBezier3DContinual(PathDataBase):
    """
    Path data class for the svg's `continual 3D bezier curve` (S).
    """

    _control_x: Int
    _control_y: Int
    _dest_x: Int
    _dest_y: Int

    def __init__(
            self,
            control_x: Union[int, Int],
            control_y: Union[int, Int],
            dest_x: Union[int, Int],
            dest_y: Union[int, Int],
            *,
            relative: bool = False):
        """
        Path data class for the svg's `continual 3D bezier curve` (S).

        Parameters
        ----------
        control_x : int or Int
            X-coordinate of the bezier's control point.
        control_y : int or Int
            Y-coordinate of the bezier's control point.
        dest_x : int or Int
            X-coordinate of the destination point.
        dest_y : int or Int
            Y-coordinate of the destination point.
        relative : bool, default False
            The boolean value indicating whether the path
            coordinates are relative or not (absolute).
        """
        from apysc._geom.path_label import PathLabel
        super(PathBezier3DContinual, self).__init__(
            path_label=PathLabel.BEZIER_3D_CONTINUAL,
            relative=relative)
        self._control_x = get_copied_int_from_builtin_val(integer=control_x)
        self._control_y = get_copied_int_from_builtin_val(integer=control_y)
        self._dest_x = get_copied_int_from_builtin_val(integer=dest_x)
        self._dest_y = get_copied_int_from_builtin_val(integer=dest_y)

    def _get_svg_str(self) -> str:
        """
        Get a path's SVG string created with the current setting.

        Returns
        -------
        svg_str : str
            A path's SVG string created with the current setting.
        """
        from apysc._type.value_util import get_value_str_for_expression
        svg_char: str = self._get_svg_char()
        control_x_str: str = get_value_str_for_expression(
            value=self._control_x)
        control_y_str: str = get_value_str_for_expression(
            value=self._control_y)
        dest_x_str: str = get_value_str_for_expression(value=self._dest_x)
        dest_y_str: str = get_value_str_for_expression(value=self._dest_y)
        svg_str: str = (
            f'"{svg_char} " + String({control_x_str}) '
            f'+ " " + String({control_y_str}) '
            f'+ " " + String({dest_x_str}) '
            f'+ " " + String({dest_y_str})'
        )
        return svg_str

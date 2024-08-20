"""
Module containing functions for plotting.
"""
from matplotlib.pyplot import figure, show, subplots, close
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.font_manager import FontProperties, get_font_names
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path
from seaborn import set as set_sea, color_palette, set_palette
from numpy import ndarray, linspace

from research_tools.in_out import get_or_create_folder
from research_tools.utils import Union, Tuple, List, Literal, update_default_dict

# Default figure/axes parameters
DEF_FIG_SIZE = (8, 5)
DEF_VIEW_DPI = 300
DEF_SAVE_DPI = 600
DEF_NUM_ROW_COL = [1, 1]
DEF_NUM_TICKS = 10

# Default font parameters
SYSTEM_FONTS = sorted(get_font_names())
DEF_FONT_NAME = 'Calibri' if 'Calibri' in SYSTEM_FONTS else SYSTEM_FONTS[0]
DEF_FONT_WEIGHTS = ['light', 'normal', 'regular', 'demibold', 'bold', 'extra bold']
DEF_FONT_STYLE = ['normal', 'italic']
DEF_FONT_SIZE = ['xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large']

# Seaborn style/colors
DEF_NUM_COLORS = 10
DEF_SEABORN_STYLE = {'context': 'paper', 'style': 'darkgrid', 'palette': 'deep', 'font': DEF_FONT_NAME,
                     'font_scale': 1.1, 'color_codes': True,
                     'rc': {'grid.linestyle': '-', 'grid.linewidth': 1.0, 'axes.edgecolor': 'black',
                            'patch.edgecolor': 'none', 'patch.linewidth': 0}}
set_sea(**DEF_SEABORN_STYLE)
set_palette(palette=DEF_SEABORN_STYLE['palette'], n_colors=DEF_NUM_COLORS,
            color_codes=DEF_SEABORN_STYLE['color_codes'])

LIST_LINE_STYLES = {'solid': (0, ()), 'dashed': (0, (5, 5)), 'dotted': (0, (1, 1)), 'dashdotted': (0, (3, 5, 1, 5)),
                    'loosely dashed': (0, (5, 10)), 'densely dashed': (0, (5, 1)), 'loosely dotted': (0, (1, 10)),
                    'loosely dashdotdotted': (0, (3, 10, 1, 10, 1, 10)),
                    'densely dashdotdotted': (0, (3, 1, 1, 1, 1, 1))}
"""Default line styles"""
LIST_MARKERS = list(Line2D.filled_markers)[1:]
"""Default list of markers"""
DEF_SHRINK_LEGEND = {'borderpad': 0.2, 'labelspacing': 0.3, 'handletextpad': 0.3, 'borderaxespad': 0.3,
                     'columnspacing': 0.8}
"""Parameters to reduce the space between handles in figure's legend"""


def get_font_property(name: str = DEF_FONT_NAME, style: str = DEF_FONT_STYLE[0],
                      weight: str = DEF_FONT_WEIGHTS[4],
                      size: Union[str, int] = DEF_FONT_SIZE[3]) -> FontProperties:
    """
    Get a font property to be used as input parameter in plot functions.

    :param name: Font name
    :param style: Font style
    :param weight: Font font_property
    :param size: Font size
    :return: Font created
    """
    if name not in SYSTEM_FONTS:
        raise ValueError('Font "{}" not installed in the system\n'
                         'List of available fonts: {}'.format(name, SYSTEM_FONTS))

    if style not in DEF_FONT_STYLE:
        raise ValueError('Font style "{}" not available\n'
                         'List of available styles: {}'.format(style, DEF_FONT_STYLE))

    return FontProperties(family=name, style=style, weight=weight, size=size)


DEFAULT_AXIS_PROPERTY = get_font_property(weight=DEF_FONT_WEIGHTS[4], size=DEF_FONT_SIZE[3])
DEFAULT_LEGEND_PROPERTY = get_font_property(weight=DEF_FONT_WEIGHTS[4], size=DEF_FONT_SIZE[1])


def get_figure(fig_id: Union[int, str] = None, size: Tuple[float, float] = DEF_FIG_SIZE,
               dpi: float = DEF_VIEW_DPI) -> Figure:
    """
    Wrapper for creation of new figure.

    :param fig_id: Figure ID
    :param size: Figure size
    :param dpi: Figure DPI
    :return: Created figure
    """
    return figure(num=fig_id, figsize=size, dpi=dpi)


def add_subplot(fig: Figure, num_rows: int = DEF_NUM_ROW_COL[0], num_columns: int = DEF_NUM_ROW_COL[1],
                index: int = 1, **kwargs) -> Axes:
    """
    Wrapper for insertion of one axis inside a figure.

    :param fig: Figure object to insert the axis
    :param num_rows: Number of rows
    :param num_columns: Number of columns
    :param index: Axis index
    :return: New axis inserted in the figure
    """
    pos = int('{}{}{}'.format(num_rows, num_columns, index), **kwargs)

    return fig.add_subplot(pos)


def add_subplot_3d(fig: Figure, num_rows: int = DEF_NUM_ROW_COL[0], num_columns: int = DEF_NUM_ROW_COL[1],
                   index: int = 1) -> Axes3D:
    """
    Wrapper for insertion of one 3-D axis inside a figure.

    :param fig: Figure object to insert the axis
    :param num_rows: Number of rows
    :param num_columns: Number of columns
    :param index: Axis index
    :return: New axis inserted in the figure
    """
    pos = int('{}{}{}'.format(num_rows, num_columns, index))

    return fig.add_subplot(pos, projection='3d')


def add_subplots(fig: Figure, num_rows: int = DEF_NUM_ROW_COL[0],
                 num_columns: int = DEF_NUM_ROW_COL[1]) -> List[Axes]:
    """
    Wrapper for insertion of all axis, defined by number of rows and columns, inside a figure.

    :param fig: Figure object to insert the axis
    :param num_rows: Number of rows
    :param num_columns: Number of columns
    :return: List of axes inserted in the figure
    """
    num_axis = num_rows * num_columns
    list_axis = []

    for index in range(1, num_axis + 1):
        list_axis.append(add_subplot(fig, num_rows, num_columns, index=index))

    return list_axis


def add_sub_axis(axis: Axes, position: Tuple[float, float, float, float], face_color='lightgray') -> Axes:
    """
    Create a sub-axis.

    :param axis: Original axis
    :param position: Position of the new axis (x0, y0, width, height)
    :param face_color: Color background of new axis
    :return: Sub-axis created
    """
    return axis.inset_axes(position, facecolor=face_color)


def get_twin(axis: Axes, axis_option: Literal['x', 'y'] = 'x') -> Axes:
    """
    Get twin axis from original axis.

    :param axis: Original axis
    :param axis_option: Define if the twin of x- or y-axis
    :return: Twin axis
    """
    if axis_option == 'x':
        return axis.twinx()
    elif axis_option == 'y':
        return axis.twiny()
    else:
        raise ValueError('Option of twin axis "{}" not valid.\n'
                         'Choose "x" of "y"')


def set_tick_labels_property(axis: Axes, font_property: FontProperties = DEFAULT_AXIS_PROPERTY):
    """
    Set all tick labels' (x and y) font weights.

    :param axis: Axis
    :param font_property: Weight option
    :return:
    """
    labels = axis.get_xticklabels() + axis.get_yticklabels()
    [label.set_fontproperties(font_property) for label in labels]


def set_labels(axis: Axes, x_label: str = None, y_label: str = None, title: str = None,
               font_property: FontProperties = DEFAULT_AXIS_PROPERTY):
    """
    Set all axis labels with the same font properties.

    :param axis: Axis
    :param x_label: Label of x-axis
    :param y_label: Label of y-axis
    :param title: Title of axis
    :param font_property: Font properties
    :return: None
    """
    if x_label:
        axis.set_xlabel(xlabel=x_label, fontproperties=font_property)
    if y_label:
        axis.set_ylabel(ylabel=y_label, fontproperties=font_property)
    if title:
        axis.set_title(label=title, fontproperties=font_property)


def set_ticks(axis: Axes, x_lims: Union[list, ndarray] = None, y_lims: Union[list, ndarray] = None,
              x_ticks: Union[int, float, list, ndarray] = None, y_ticks: Union[int, float, list, ndarray] = None,
              x_ticks_labels: Union[int, float, list, ndarray] = None,
              y_ticks_labels: Union[int, float, list, ndarray] = None,
              font_properties: FontProperties = DEFAULT_AXIS_PROPERTY):
    """
    Set both axis limits, ticks and tick labels.
    If the limits are not provided, use the axis limits.
    If both ticks and tick labels and not provided, creating 10 points between the limits.
    If only the ticks are provided, replicate the ticks for the labels.
    Does not accept ticks labels only.
    Uses the same font properties for both axes.

    :param axis: Axes
    :param x_lims: Limits along x-axis
    :param y_lims: Limits along y-axis
    :param x_ticks: X-axis ticks
    :param y_ticks: Y-axis ticks
    :param x_ticks_labels: X-axis ticks labels
    :param y_ticks_labels: Y-axis ticks labels
    :param font_properties: Font properties
    :return: None
    """
    # Set x-axis limits
    if x_lims is None:
        x_lims = axis.get_xlim()
    else:
        axis.set_xlim(*x_lims)

    # Set y-axis limits
    if y_lims is None:
        y_lims = axis.get_ylim()
    else:
        axis.set_ylim(*y_lims)

    # Configure and set x-axis ticks and ticks labels
    if x_ticks is None and x_ticks_labels is None:
        x_ticks = linspace(x_lims[0], x_lims[1], DEF_NUM_TICKS)
        x_ticks_labels = x_ticks
    elif x_ticks_labels is None:
        x_ticks_labels = x_ticks
    elif x_ticks is None:
        raise ValueError('If x_ticks_labels is provided, requires also x_ticks')
    axis.set_xticks(x_ticks)
    axis.set_xticklabels(x_ticks_labels, fontproperties=font_properties)

    # Configure and set x-axis ticks and ticks labels
    if y_ticks is None and y_ticks_labels is None:
        y_ticks = linspace(y_lims[0], y_lims[1], DEF_NUM_TICKS)
        y_ticks_labels = y_ticks
    elif y_ticks_labels is None:
        y_ticks_labels = y_ticks
    elif y_ticks is None:
        raise ValueError('If y_ticks_labels is provided, requires also y_ticks')
    axis.set_yticks(y_ticks)
    axis.set_yticklabels(y_ticks_labels, fontproperties=font_properties)


def set_legend(axis: Axes, position: str = 'best', title: str = None,
               font_properties: FontProperties = DEFAULT_LEGEND_PROPERTY, shrink=False, **kwargs) -> Legend:
    """
    Set axis legend and legend title, both using the same font properties.

    :param axis: Axis
    :param position: Legend position
    :param title: Legend title
    :param font_properties: Font properties
    :param shrink: Option to reduce the space between legend name, makers, pads, etc.
    :param kwargs: Keyword arguments
    :return:
    """
    # TODO: Add option for manual handles
    if shrink:
        kwargs = update_default_dict(DEF_SHRINK_LEGEND, kwargs)
    legend = axis.legend(loc=position, prop=font_properties, **kwargs)
    legend.set_title(title=title, prop=font_properties)

    return legend


def save_fig(fig_path: Union[Path, str], fig: Figure, bbox_inches='tight', dpi=DEF_SAVE_DPI):
    """
    Save figure

    :param fig_path: File path
    :param fig: Figure object
    :param bbox_inches: Parameter to bounding box in inches (tight = tight bbox of the figure)
    :param dpi: DPI applied to the figure
    :return:
    """
    fig.savefig(fname=fig_path, bbox_inches=bbox_inches, dpi=dpi)


def save_figs_pdf(fig_path: Union[Path, str], list_figs: List[Figure], bbox_inches='tight', dpi=DEF_SAVE_DPI):
    """
    Save a list of figures in a single .pdf file, one by page.

    :param fig_path: File path
    :param list_figs: List of figures to save
    :param bbox_inches: Parameter to bounding box in inches (tight = tight bbox of the figure)
    :param dpi: DPI applied to the figure
    :return:
    """
    if not Path(fig_path).suffix == '.pdf':
        raise TypeError('".{}" is not an accepted format, only ".pdf"'.format(Path(fig_path).suffix))

    with PdfPages(fig_path) as pdf:
        for fig in list_figs:
            pdf.savefig(figure=fig, **{'bbox_inches': bbox_inches, 'dpi': dpi})


def set_get_color_list(palette=DEF_SEABORN_STYLE['palette'], n_colors=DEF_NUM_COLORS):
    """
    Set the seaborn color palette and return the list of colors.

    :param palette: Seaborn palette.
    :param n_colors: Number of colors
    :return: List of colors
    """
    set_palette(palette=palette, n_colors=n_colors)
    return color_palette(palette=palette, n_colors=n_colors)


def update_style(new_params: Union[None, dict] = None):
    """
    Update seaborn style

    :param new_params: Parameter to update seaborn
    :return:
    """
    if new_params is None:
        new_params = DEF_SEABORN_STYLE
    set_sea(**new_params)


def get_list_line_styles(num_styles: int = None):
    """
    Return a dict containing the line styles names and values. If no number of line is provided, return the whole dict
    defined in this module.

    :param num_styles: Number of line styles
    :return: Dict containing the line styles
    """
    if num_styles is None or num_styles > len(LIST_LINE_STYLES):
        return LIST_LINE_STYLES
    else:
        return {key: value for (key, value), _ in zip(LIST_LINE_STYLES.items(), range(0, num_styles))}


def get_list_markers(num_markers: int = None):
    """
    Return a list of filled markers types. If no number of markers is provided, return the whole list defined in
    this module.

    :param num_markers: Number of markers
    :return: List of filled markers
    """
    if num_markers is None or num_markers > len(LIST_MARKERS):
        return LIST_MARKERS
    else:
        return LIST_MARKERS[:num_markers - 1]


if __name__ == '__main__':
    import numpy as np

    x_axis = np.arange(start=0, stop=10, step=0.1)
    color_list = set_get_color_list()

    # Creation of first figure with two axes, created separately
    fig1 = get_figure()
    ax1 = add_subplot(fig=fig1, num_rows=1, num_columns=2, index=1)
    ax2 = add_subplot(fig1, 1, 2, 2)
    ax1.plot(x_axis, np.sin(x_axis), color=color_list[0], label='Sin')
    ax2.plot(x_axis, np.cos(x_axis), color=color_list[1], label='Cos')
    new_ax_2 = get_twin(ax2, axis_option='y')
    new_ax_2.plot(x_axis + 10, np.sin(x_axis + 10), color=color_list[2], label='Sin')

    font_legend1 = get_font_property()
    font_legend2 = get_font_property(weight=DEF_FONT_WEIGHTS[1])
    ax2.legend(loc='lower center', prop=font_legend1)
    new_ax_2.legend(loc='upper right', prop=font_legend2)

    font_label1 = get_font_property(weight=DEF_FONT_WEIGHTS[1])
    ax1.set_xlabel('x', fontproperties=font_label1)
    font_label2 = get_font_property(weight=DEF_FONT_WEIGHTS[5])
    ax1.set_ylabel('Sin(x)', fontproperties=font_label2)

    set_tick_labels_property(ax1)

    fig1.tight_layout()

    # Creation of second figure with four axes, created all together
    fig2 = get_figure()
    ax_list = add_subplots(fig2, 2, 2)
    ax_list[0].plot(x_axis, np.sin(x_axis), color=color_list[3])
    ax_list[0].plot(x_axis, np.cos(x_axis), color=color_list[4])
    ax_list[0].plot(x_axis, np.exp(-x_axis), color=color_list[6])
    ax_list[1].plot(x_axis, np.tan(x_axis), color=color_list[5])
    ax_list[2].plot(x_axis, np.sinh(x_axis), color=color_list[6])
    ax_list[3].plot(x_axis, np.cosh(x_axis), color=color_list[7])

    fig2.tight_layout()

    # Save figure(s)
    out_path = get_or_create_folder('../dump_data/Figures')
    save_fig(fig_path=out_path / 'sin_cos.png', fig=fig1)
    save_figs_pdf(fig_path=out_path / 'all_plots.pdf', list_figs=[fig1, fig2])

    show()

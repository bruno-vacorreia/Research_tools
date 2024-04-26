from matplotlib.pyplot import figure, show
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.font_manager import FontProperties, get_font_names
from pathlib import Path
from seaborn import set as set_sea, color_palette, set_palette, axes_style

from personal_tools.in_out import get_or_create_folder
from personal_tools.utils import Union, Tuple, List, Literal

# Default figure/axes parameters
DEF_FIG_SIZE = (8, 5)
DEF_VIEW_DPI = 300
DEF_SAVE_DPI = 600
DEF_NUM_ROW_COL = [1, 1]

# Default font parameters
SYSTEM_FONTS = sorted(get_font_names())
DEF_FONT_NAME = 'Calibri'
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

# Default line styles
LIST_LINE_STYLES = {'solid': (0, ()), 'dashed': (0, (5, 5)), 'dotted': (0, (1, 1)), 'dashdotted': (0, (3, 5, 1, 5)),
                    'loosely dashed': (0, (5, 10)), 'densely dashed': (0, (5, 1)), 'loosely dotted': (0, (1, 10)),
                    'loosely dashdotdotted': (0, (3, 10, 1, 10, 1, 10)),
                    'densely dashdotdotted': (0, (3, 1, 1, 1, 1, 1))}


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
                index: int = 1) -> Axes:
    """
    Wrapper for insertion of one axis inside a figure.

    :param fig: Figure object to insert the axis
    :param num_rows: Number of rows
    :param num_columns: Number of columns
    :param index: Axis index
    :return: New axis inserted in the figure
    """
    pos = int('{}{}{}'.format(num_rows, num_columns, index))

    return fig.add_subplot(pos)


def add_subplots(fig: Figure, num_rows: int = DEF_NUM_ROW_COL[0],
                 num_columns: int = DEF_NUM_ROW_COL[1]) -> List[Axes]:
    """
    Wrapper for insertion of all axis, defined by number of rows and columns, inside a figure

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
    Create a sub-axis

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


def set_labels_weight(axis: Axes, weight=DEF_FONT_WEIGHTS[4]):
    """
    Set all tick labels' (x and y) font weights.

    :param axis: Axis
    :param weight: Weight option
    :return:
    """
    labels = axis.get_xticklabels() + axis.get_yticklabels()
    [label.set_fontweight(weight) for label in labels]


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


def get_font_property(name: str = DEF_FONT_NAME, style: str = DEF_FONT_STYLE[0],
                      weight: str = DEF_FONT_WEIGHTS[4],
                      size: Union[str, int] = DEF_FONT_SIZE[3]) -> FontProperties:
    """
    Get a font property to be used as input parameter in plot functions.

    :param name: Font name
    :param style: Font style
    :param weight: Font weight
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


def set_axes_labels(axis: Axes, x_label: str, y_label: str, title: str = None, font_property: FontProperties = None,
                    **kwargs):
    """
    Set the axis labels, both x and y, and title (optional).
    If the font property is not set, use the default font properties.

    :param axis: Axis object
    :param x_label: X label
    :param y_label: Y label
    :param title: Axis title (Optional)
    :param font_property: Font properties (Optional)
    :param kwargs:
    :return:
    """
    if font_property is None:
        font_property = get_font_property()
    axis.set_xlabel(xlabel=x_label, fontproperties=font_property, **kwargs)
    axis.set_ylabel(ylabel=y_label, fontproperties=font_property, **kwargs)

    if title is not None:
        axis.set_title(title=title, fontproperties=font_property, **kwargs)


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

    set_labels_weight(ax1)

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

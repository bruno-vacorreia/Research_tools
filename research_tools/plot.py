"""
Module containing functions for plotting.
"""
from pathlib import Path
from matplotlib.axes import Axes
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties, get_font_names
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.pyplot import figure, show, rc
from mpl_toolkits.mplot3d import Axes3D
from numpy import ndarray
from seaborn import color_palette, set_palette, set_theme

from research_tools.in_out import get_or_create_folder
from research_tools.utils import Union, Tuple, List, Literal, update_default_dict

# Default figure/axes parameters
DEF_FIG_SIZE = (8, 5)
DEF_VIEW_DPI = 300
DEF_SAVE_DPI = 600
DEF_NUM_ROW_COL = [1, 1]

# Default font parameters
SYSTEM_FONTS = sorted(get_font_names())
DEF_FONT_NAME = 'Calibri' if 'Calibri' in SYSTEM_FONTS else SYSTEM_FONTS[0]
LIST_FONT_WEIGHTS = ['light', 'normal', 'regular', 'demibold', 'bold', 'extra bold']
LIST_FONT_STYLE = ['normal', 'italic']
LIST_FONT_SIZE = ['xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large']

# Seaborn style/colors
DEF_NUM_COLORS = 10
DEF_SEABORN_STYLE = {
    'context': 'paper',
    'style': 'darkgrid',
    'palette': 'deep',
    'font': DEF_FONT_NAME,
    'font_scale': 1.1,
    'color_codes': True,
    'rc': {'grid.linestyle': '-',
           'grid.linewidth': 1.0,
           'axes.edgecolor': 'black',
           'patch.edgecolor': 'black',
           'patch.linewidth': 0}
}
set_theme(**DEF_SEABORN_STYLE)
set_palette(palette=DEF_SEABORN_STYLE['palette'], n_colors=DEF_NUM_COLORS, color_codes=DEF_SEABORN_STYLE['color_codes'])
# Parameters for font type error in papers
rc('pdf', fonttype=42)
rc('ps', fonttype=42)

LIST_LINE_STYLES = {
    'solid': (0, ()),
    'dashed': (0, (5, 5)),
    'dotted': (0, (1, 1)),
    'dashdotted': (0, (3, 5, 1, 5)),
    'loosely dashed': (0, (5, 10)),
    'densely dashed': (0, (5, 1)),
    'loosely dotted': (0, (1, 10)),
    'loosely dashdotdotted': (0, (3, 10, 1, 10, 1, 10)),
    'densely dashdotdotted': (0, (3, 1, 1, 1, 1, 1))
}
"""List of default line styles"""
LIST_MARKERS = list(Line2D.filled_markers)[1:]
"""List of default markers"""
LIST_SHRINK_OPTIONS = {
    'low': {
        'borderpad': 0.3,
        'labelspacing': 0.4,
        'handlelength': 1.5,
        'handleheight': 0.5,
        'handletextpad': 0.6,
        'borderaxespad': 0.4,
        'columnspacing': 1.5
    },
    'medium': {
        'borderpad': 0.2,
        'labelspacing': 0.3,
        'handlelength': 1.0,
        'handleheight': 0.3,
        'handletextpad': 0.4,
        'borderaxespad': 0.3,
        'columnspacing': 1.0
    },
    'high': {
        'borderpad': 0.1,
        'labelspacing': 0.2,
        'handlelength': 0.5,
        'handleheight': 0.1,
        'handletextpad': 0.2,
        'borderaxespad': 0.1,
        'columnspacing': 0.5
    }
}
"""Parameters to reduce the space between handles in figure's legend"""


def get_font_property(name: str = DEF_FONT_NAME, style: str = LIST_FONT_STYLE[0],
                      weight: str = LIST_FONT_WEIGHTS[4],
                      size: Union[str, int] = LIST_FONT_SIZE[3], **kwargs) -> FontProperties:
    """
    Get a font property to be used as input parameter in plot functions.

    :param name: Font name
    :param style: Font style
    :param weight: Font font_property
    :param size: Font size
    :return: Font created
    """
    if name not in SYSTEM_FONTS:
        raise ValueError(f'Font "{name}" not installed in the system\n'
                         f'List of available fonts: {SYSTEM_FONTS}')

    if style not in LIST_FONT_STYLE:
        raise ValueError(f'Font style "{style}" not available\n'
                         f'List of available styles: {LIST_FONT_STYLE}')

    return FontProperties(family=name, style=style, weight=weight, size=size, **kwargs)


DEFAULT_AXIS_PROPERTY = get_font_property(weight=LIST_FONT_WEIGHTS[4], size=LIST_FONT_SIZE[3])
DEFAULT_LEGEND_PROPERTY = get_font_property(weight=LIST_FONT_WEIGHTS[4], size=LIST_FONT_SIZE[1])


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
    pos = int(f'{num_rows}{num_columns}{index}')

    return fig.add_subplot(pos, **kwargs)


def add_subplot_3d(fig: Figure, num_rows: int = DEF_NUM_ROW_COL[0], num_columns: int = DEF_NUM_ROW_COL[1],
                   index: int = 1, **kwargs) -> Axes3D:
    """
    Wrapper for insertion of one 3-D axis inside a figure.

    :param fig: Figure object to insert the axis
    :param num_rows: Number of rows
    :param num_columns: Number of columns
    :param index: Axis index
    :return: New axis inserted in the figure
    """
    pos = int(f'{num_rows}{num_columns}{index}')

    return fig.add_subplot(pos, projection='3d', **kwargs)


def add_subplots(fig: Figure, num_rows: int = DEF_NUM_ROW_COL[0],
                 num_columns: int = DEF_NUM_ROW_COL[1], **kwargs) -> List[Axes]:
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
        list_axis.append(add_subplot(fig, num_rows, num_columns, index=index, **kwargs))

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


def set_labels(axis: Axes, x_label: str = None, y_label: str = None, title: str = None,
               font_property: FontProperties = DEFAULT_AXIS_PROPERTY, **kwargs):
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
        axis.set_xlabel(xlabel=x_label, fontproperties=font_property, **kwargs)
    if y_label:
        axis.set_ylabel(ylabel=y_label, fontproperties=font_property, **kwargs)
    if title:
        axis.set_title(label=title, fontproperties=font_property, **kwargs)


def set_fig_super_title(fig: Figure, title: str, font_property: FontProperties = DEFAULT_AXIS_PROPERTY,
                        **kwargs):
    """
    Set figure title, if working with multiple subplots and requires a single title for the entire figure.

    :param fig: Figure
    :param title: Title text
    :param font_property: Font properties
    :return:
    """
    fig.suptitle(t=title, fontproperties=font_property, **kwargs)


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
    if x_lims is not None:
        axis.set_xlim(*x_lims)

    # Set y-axis limits
    if y_lims is not None:
        axis.set_ylim(*y_lims)

    # Configure and set x-axis ticks and ticks labels
    if x_ticks is None and x_ticks_labels is None:
        x_ticks = axis.get_xticks()
        x_ticks_labels = axis.get_xticklabels()
    elif x_ticks_labels is None:
        x_ticks_labels = x_ticks
    elif x_ticks is None:
        raise ValueError('If x_ticks_labels is provided, requires also x_ticks')
    axis.set_xticks(x_ticks)
    axis.set_xticklabels(x_ticks_labels, fontproperties=font_properties)

    # Configure and set x-axis ticks and ticks labels
    if y_ticks is None and y_ticks_labels is None:
        y_ticks = axis.get_yticks()
        y_ticks_labels = axis.get_yticklabels()
    elif y_ticks_labels is None:
        y_ticks_labels = y_ticks
    elif y_ticks is None:
        raise ValueError('If y_ticks_labels is provided, requires also y_ticks')
    axis.set_yticks(y_ticks)
    axis.set_yticklabels(y_ticks_labels, fontproperties=font_properties)


def set_legend(axis: Axes, handles: List[Union[Line2D, Patch]] = None, position: str = 'best', title: str = None,
               font_properties: FontProperties = DEFAULT_LEGEND_PROPERTY,
               shrink: Union[bool, str] = False, **kwargs) -> Legend:
    """
    Set axis legend and legend title, both using the same font properties.

    :param axis: Axis
    :param handles: List of handles to set manually
    :param position: Legend position
    :param title: Legend title
    :param font_properties: Font properties
    :param shrink: Option to reduce the space between legend name, makers, pads, etc.
    If set as True, will apply the low shrink option. It accepts also low, medium and high options.
    :param kwargs: Keyword arguments
    :return:
    """
    # Shrink option
    if isinstance(shrink, bool) and shrink is True:
        kwargs = update_default_dict(LIST_SHRINK_OPTIONS['low'], kwargs)
    elif isinstance(shrink, str) and shrink in LIST_SHRINK_OPTIONS.keys():
        kwargs = update_default_dict(LIST_SHRINK_OPTIONS[shrink], kwargs)
    elif isinstance(shrink, str) and shrink not in LIST_SHRINK_OPTIONS.keys():
        raise NotImplementedError(f'Invalid option "{shrink}" for shrink\n'
                                  f'Options are {list(LIST_SHRINK_OPTIONS.keys())}')

    if handles is not None:
        legend = axis.legend(handles=handles, loc=position, prop=font_properties, **kwargs)
    else:
        legend = axis.legend(loc=position, prop=font_properties, **kwargs)

    if title is not None:
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
    Update seaborn style.

    :param new_params: Parameter to update seaborn
    :return:
    """
    if new_params is None:
        new_params = DEF_SEABORN_STYLE
    set_theme(**new_params)


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
    list_colors = set_get_color_list(n_colors=12)
    list_markers = get_list_markers()

    # Creation of first figure with two axes, created separately
    fig1 = get_figure()
    ax1 = add_subplot(fig=fig1, num_rows=1, num_columns=2, index=1)
    ax2 = add_subplot(fig1, 1, 2, 2)
    ax1.plot(x_axis, np.sin(x_axis), color=list_colors[0], marker=list_markers[0], label='Sin')
    ax2.plot(x_axis, np.cos(x_axis), color=list_colors[1], marker=list_markers[1], label='Cos')
    new_ax_2 = get_twin(ax2, axis_option='y')
    new_ax_2.plot(x_axis + 10, np.sin(x_axis + 10), color=list_colors[2], label='Sin')

    font_legend1 = get_font_property()
    font_legend2 = get_font_property(weight=LIST_FONT_WEIGHTS[1])
    set_legend(axis=ax2, position='lower center', font_properties=font_legend1)
    set_legend(axis=new_ax_2, position='upper right', font_properties=font_legend2, shrink=True)

    font_label1 = get_font_property(weight=LIST_FONT_WEIGHTS[1])
    font_label2 = get_font_property(weight=LIST_FONT_WEIGHTS[5])
    set_labels(axis=ax1, x_label='x', font_property=font_label1)
    set_labels(axis=ax1, x_label='Sin(x)', font_property=font_label2)

    ax1.set_xlabel('x', fontproperties=font_label1)
    ax1.set_ylabel('Sin(x)', fontproperties=font_label2)

    set_fig_super_title(fig1, title='Example of twin axes and different font for labels and legend')
    fig1.tight_layout()

    # Creation of figure with example of shrink label options
    fig2 = get_figure()
    ax_list = add_subplots(fig2, 2, 2)
    ax_list[0].plot(x_axis, np.sin(x_axis), color=list_colors[0], marker=list_markers[0], label='sin')
    ax_list[0].plot(x_axis, np.cos(x_axis), color=list_colors[1], marker=list_markers[1], label='cos')
    ax_list[0].plot(x_axis, np.exp(-x_axis), color=list_colors[2], marker=list_markers[2], label='exp')
    set_legend(axis=ax_list[0], position='lower left', font_properties=font_label2, shrink=False)

    ax_list[1].plot(x_axis, np.sin(x_axis), color=list_colors[3], marker=list_markers[3], label='sin')
    ax_list[1].plot(x_axis, np.cos(x_axis), color=list_colors[4], marker=list_markers[4], label='cos')
    ax_list[1].plot(x_axis, np.exp(-x_axis), color=list_colors[5], marker=list_markers[5], label='exp')
    set_legend(axis=ax_list[1], position='lower left', font_properties=font_label2, shrink='low')

    ax_list[2].plot(x_axis, np.sin(x_axis), color=list_colors[6], marker=list_markers[6], label='sin')
    ax_list[2].plot(x_axis, np.cos(x_axis), color=list_colors[7], marker=list_markers[7], label='cos')
    ax_list[2].plot(x_axis, np.exp(-x_axis), color=list_colors[8], marker=list_markers[8], label='exp')
    set_legend(axis=ax_list[2], position='lower left', font_properties=font_label2, shrink='medium')

    ax_list[3].plot(x_axis, np.sin(x_axis), color=list_colors[9], marker=list_markers[9], label='sin')
    ax_list[3].plot(x_axis, np.cos(x_axis), color=list_colors[10], marker=list_markers[10], label='cos')
    ax_list[3].plot(x_axis, np.exp(-x_axis), color=list_colors[11], marker=list_markers[11], label='exp')
    set_legend(axis=ax_list[3], position='lower left', font_properties=font_label2, shrink='high')

    set_fig_super_title(fig2, title='Example of shrink legend')
    fig2.tight_layout()

    # Save figure(s)
    out_path = get_or_create_folder('../dump_data/Figures')
    # save_fig(fig_path=out_path / 'sin_cos.png', fig=fig1)
    # save_figs_pdf(fig_path=out_path / 'all_plots.pdf', list_figs=[fig1, fig2])

    show()

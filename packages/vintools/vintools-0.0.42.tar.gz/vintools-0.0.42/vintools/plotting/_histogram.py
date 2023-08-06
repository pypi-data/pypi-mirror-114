import matplotlib.pyplot as plt

def _style_simple_histogram(
    title="Array Distribution",
    x_lab="Range",
    y_lab="Count",
    size=(5, 4),
    title_fontsize=12,
    title_adjustment_factor=1.1,
    axis_label_fontsize=8,
):

    fig = plt.figure(figsize=size)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title(title, fontsize=title_fontsize, y=title_adjustment_factor)
    ax.set_xlabel(x_lab, fontsize=axis_label_fontsize)
    ax.set_ylabel(y_lab, fontsize=axis_label_fontsize)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_linewidth(2)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.xaxis.set_ticks_position("bottom")
    ax.yaxis.set_visible(False)

    return fig, ax


def _annotate_histogram(bin_annotation, alt_x=False, alt_y=False, alt_text=False):

    """Annotate a histogram with text. Default to annotating max value."""

    dist = bin_annotation[0]
    x_pos = 0
    y_pos = dist.max() * 1.05
    plot_text = "Max:{}".format(dist.max())

    if alt_x:
        x_pos = alt_x
    if alt_y:
        y_pos = alt_y
    if alt_text:
        x_pos = alt_text

    plt.text(x=x_pos, y=y_pos, s=plot_text)


def _plot_histogram(array, n_bins=20, color='#9ABD76'):

    _style_simple_histogram()
    bins = plt.hist(array, bins=n_bins, color=color)
    _annotate_histogram(bin_annotation=bins)
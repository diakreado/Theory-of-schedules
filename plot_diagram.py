from matplotlib import pyplot as plt
import matplotlib.patches as patches
import numpy as np


def get_plot_data(t, works):

    number_of_workers = len(works[0])

    for i in range(len(works)):
        works[i] = works[i].tolist()
    current_works = works[0][:]

    mapped_works = []

    for j in range(len(t) - 1):

        for i in range(len(current_works)):
            if current_works[i] not in works[j]:
                current_works[i] = None
            else:
                works[j].remove(current_works[i])

        for i in range(len(current_works)):
            if current_works[i] is None and len(works[j]) > 0:
                current_works[i] = works[j][0]
                works[j].remove(current_works[i])

        mapped_works.append(current_works[:])

    empty = []
    for i in range(number_of_workers):
        empty.append(None)
    mapped_works.append(empty)

    # t.append(t[-1])

    switches = []
    labels = []
    for i in range(number_of_workers):
        switches.append([])
        labels.append([])

    for i in range(len(mapped_works) - 1):
        for j in range(number_of_workers):
            if mapped_works[i][j] != mapped_works[i + 1][j]:
                switches[j].append(t[i + 1])
                label = str(mapped_works[i][j])
                label = label.replace('None', '')
                label = label.replace(',', '')
                labels[j].append(label)

    return switches, labels


def get_rect(start, end, color=None):
    fill_rect = color is not None
    return patches.Rectangle((start, 0.0), end - start, 0.6, fill=fill_rect, facecolor=color)


def plot_diagram(t, works, number_of_workers):

    space_betw_rects = 0.1

    fig, ax = plt.subplots(number_of_workers, sharex=False, sharey=True, figsize=(16, 5.8))

    for axes in ax:
        axes.tick_params(axis='both', labelsize=16)
        axes.set_xticks(t)
        axes.set_yticks([])
        for side in ['bottom', 'right', 'top', 'left']:
            axes.spines[side].set_visible(False)
        axes.axhline(linewidth=1.5, color="black")
        axes.set_xlim([t[0], t[-1]])
        axes.set_ylim([0, 1])

    sw, lb = get_plot_data(t, works)

    print(sw, lb)

    t_start = []
    t_end = []

    for i in range(number_of_workers):
        t_start.append(t[0])
        t_end.append(t[0])

    for j in range(number_of_workers):
        for i in range(len(sw[j])):
            t_end[j] = sw[j][i]
            if lb[j][i] != '':
                ax[j].add_patch(get_rect(t_start[j] + space_betw_rects / 2, t_end[j] - space_betw_rects / 2))
            ax[j].text(t_start[j] + (t_end[j] - t_start[j]) / 2, 0.3, lb[j][i],
                       horizontalalignment='center', verticalalignment='center', fontsize=16)
            t_start[j] = t_end[j]

    plt.savefig("diag.png", bbox_inches='tight')
    plt.show()



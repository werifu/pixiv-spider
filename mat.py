import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False


def plt_barh(author_illust:dict, tag):
    authors = author_illust.keys()
    nums = author_illust.values()

    plt.barh(range(len(author_illust)), nums, height=1, color='steelblue', alpha=0.8)
    plt.yticks(range(len(author_illust)), authors)
    plt.xlim(0, 25)
    plt.xlabel('数量')
    plt.title(tag)
    for x, y in enumerate(nums):
        plt.text(y + 0.2, x - 0.1, "%s" % y)
    plt.show()
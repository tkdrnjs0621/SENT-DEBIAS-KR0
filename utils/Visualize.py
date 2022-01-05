import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

def Visualize(fontpath, size, original_avg_2d, debiased_avg_2d):
    fontprop = fm.FontProperties(fname=fontpath, size=9)

    x = [p[0] for p in original_avg_2d.values()]
    y = [p[1] for p in original_avg_2d.values()]
    x2 = [p[0] for p in debiased_avg_2d.values()]
    y2 = [p[1] for p in debiased_avg_2d.values()]

    plt.rcParams["figure.figsize"] = (14,14)
    fig = plt.figure()

    ax = fig.add_subplot(2,2,1)
    ax.set_title("original")
    ax.scatter(x,y)

    ax2 = fig.add_subplot(2,2,2)
    ax2.set_title("debiased")
    ax2.scatter(x2,y2)

    for i, txt in enumerate(original_avg_2d.keys()):
        ax.annotate(txt, (x[i], y[i]),fontproperties=fontprop)

    for i, txt in enumerate(debiased_avg_2d.keys()):
        ax2.annotate(txt, (x2[i], y2[i]),fontproperties=fontprop)

    plt.show()
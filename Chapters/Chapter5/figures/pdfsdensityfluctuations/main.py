# %%
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import kitcolors as kit

# %%


def pareto(s, s0=1, alpha=3):
    if s <= s0:
        return 0
    else:
        return alpha*s0**alpha/s**(1+alpha)


def Pareto(s, s0=1, alpha=3):
    if s <= s0:
        return 0
    else:
        return 1-(alpha / s)**alpha


def gamma(s):
    return s*np.exp(-s)


def Gamma(s):
    return 1-(1+s)*np.exp(-s)


def setting1(x):
    if x < 2:
        return 1
    else:
        return 2


def setting2(x):
    if x < 2:
        return 2
    else:
        return 1


def setting3(x):
    return 1.5


def compute_pdf(s, rho, pdf, x0=0):
    y = np.empty_like(s)
    def integrand(s): return rho(x0+s)
    for i, si in enumerate(s):
        opticallength, _ = quad(integrand, 0, si)
        y[i] = rho(x0+si)*pdf(opticallength)
    return y


def compute_crosssections(s, rho, pdf, cdf, x0=0):
    y = np.empty_like(s)
    enumerator = compute_pdf(s, rho, pdf, x0)
    def integrand(s): return rho(x0+s)
    for i, si in enumerate(s):
        opticallength, _ = quad(integrand, 0, si)
        denominator = 1-cdf(opticallength)
        y[i] = enumerator[i] / denominator
    return y


# %%

if True:
    pdf = gamma
    cdf = Gamma
    color = kit.purple
    name = "gamma"
    n = 1000
    s = np.linspace(0, 5, n)

else:
    pdf = pareto
    cdf = Pareto
    color = kit.orange
    name = "pareto"
    n = 1000
    s = np.linspace(0, 3, n)


pdf1 = compute_pdf(s, setting1, pdf)
pdf2 = compute_pdf(s, setting2, pdf)
pdf3 = compute_pdf(s, setting3, pdf)
cs1 = compute_crosssections(s, setting1, pdf, cdf)
cs2 = compute_crosssections(s, setting2, pdf, cdf)
cs3 = compute_crosssections(s, setting3, pdf, cdf)

# %%

l1 = "$p(s,\mathbf{x}, \mathbf{\Omega})$"
l2 = "$\sigma(s,\mathbf{x}, \mathbf{\Omega})$"

for plotid, (word, namei, label, y1, y2, y3, col) in enumerate(zip(["Path length distributions", "Cross sections"], [name+"pdf", name+"cs"], [l1, l2], [pdf1, cs1], [pdf2, cs2], [pdf3, cs3], [color, color])):
    plt.style.use("kitish")
    fig, ax = plt.subplots()
    ax.plot(s, y1, c=kit.black, linestyle="dotted", label="$ \\rho_1$")
    ax.plot(s, y2, c=kit.black, linestyle="dashed", label="$ \\rho_2$")
    ax.plot(s, y3, c=kit.black, linestyle="solid", label="$ \\rho_3$ ")

    c1, c2 = color, color
    # ax.text(1, 0.22, "Material $1$", ha="center", color=c1,
    #        bbox=dict(facecolor='white', edgecolor="w", boxstyle='round,pad=0.3'))
    # ax.text(4, 0.22, "Material $2$", ha="center", color=c2,
    #        bbox=dict(facecolor="w", edgecolor="w", boxstyle='round,pad=0.3'))

    upper = max([np.max(y1), np.max(y2), np.max(y3)])+1
    rect = Rectangle((0, 0), 2, upper)
    pc1 = PatchCollection([rect], facecolor=c1, alpha=0.3, edgecolor=c1)
    ax.add_collection(pc1)
    rect = Rectangle((2, 0), 3, upper)
    pc2 = PatchCollection([rect], facecolor=c2, alpha=0.1,  edgecolor=c2)
    ax.add_collection(pc2)
    #ax.set_yscale("log")
    ax.legend()
    ax.set_xlabel("$s$")
    ax.set_ylabel(label)
    ax.set_title("{} for a domain with one interface".format(word))
    plt.savefig(namei+".pdf")

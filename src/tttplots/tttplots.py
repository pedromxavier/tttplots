# Standard Library
import argparse
import csv
import shutil

# Third-party
import matplotlib.pyplot as plt
import numpy as np
import scienceplots

# Local
from .version import __version__, __python_version__


def has_latex():
    return shutil.which("latex") is not None


def plot_series(t: np.ndarray, name: str, npoints: int = 100):
    n = len(t)
    T = max(t)
    p = np.array([(i + 0.5) / (n + 1) for i in range(n)])

    # Lower Quantile
    ql = int(0.25 * (n + 1))
    zl = t[ql]
    wl = -np.log(1 - p[ql])

    # Upper Quantile
    qu = int(0.75 * (n + 1))
    zu = t[qu]
    wu = -np.log(1 - p[qu])

    # Distribution parameters
    λ = (zu - zl) / (wu - wl)
    μ = zl - λ * wl
    ε = T / npoints

    # Theoretical Curve
    t_t = np.array([i * ε for i in range(npoints)])
    t_p = np.array([1 - np.exp((μ - i * ε) / λ) for i in range(npoints)])

    # Theoretical Plot
    plt.plot(t_t, t_p, "--")

    # Empirical Plot
    plt.scatter(t, p, marker="+", label=name)


def tttplot(dst_path: str, name_list: list, path_list: list, npoints: int = 100):
    # Configure Plot
    plt.figure(figsize=(5, 4))

    if has_latex():
        plt.style.use(["science"])
    else:
        plt.style.use(["science", "no-latex"])

    # Plot Text
    plt.title("Time-to-target Plot")

    plt.xlabel("Time (sec)")
    plt.ylabel("Cumulative Probability")

    plt.ylim(0.0, 1.0)

    for name, path in zip(name_list, path_list):
        with open(path, "r") as file:
            t = np.array(sorted(map(lambda l: float(l.strip()), file)))

            plot_series(t, name, npoints)

    # Add plot legend
    plt.legend()

    # Save to PDF
    plt.savefig(dst_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--out", default="figure.pdf")
    parser.add_argument(
        "-s", "--src", nargs=2, metavar=("name", "path"), action="append"
    )
    parser.add_argument("-n", "--npoints", default=100, type=int)
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__} (Python {__python_version__})",
    )

    args = parser.parse_args()

    if args.src is None:
        parser.error("No input provided")

    name_list = []
    path_list = []

    for (name, path) in args.src:
        name_list.append(name)
        path_list.append(path)

    tttplot(args.out, name_list, path_list, args.npoints)
    
    exit(0)

import argparse
import csv


def extract(target: float, path_list: list, dst_path: str):
    tt = []

    for path in path_list:
        zt = []

        with open(path, "r") as fp:
            for row in csv.DictReader(fp):
                zt.append(row["t"], row["z"])

        zt.sort()

        for z, t in zt:
            if z >= target:
                tt.append(t)

    with open(dst_path, "w") as fp:
        print("\n".join(map(str, tt)), file=fp)
    
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--out", default="results.dat")
    parser.add_argument("target", type=float)
    parser.add_argument("path", nargs="+")

    args = parser.parse_args()

    extract(args.target, args.path, args.out)

    exit(0)

import argparse
import csv
import glob


def extract(target: float, path_list: list, dst_path: str):
    tt = []

    for path in path_list:
        zt = []

        with open(path, "r") as fp:
            for row in csv.DictReader(fp):
                zt.append((float(row["t"]), float(row["z"])))

        zt.sort()

        for t, z in zt:
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

    path_list = []

    for path in args.path:
        path_list.extend(glob.glob(path))

    extract(args.target, path_list, args.out)

    exit(0)

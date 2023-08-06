import argparse
import ast
import os
from fetching import fetch


def write_output(dest: str, content: str):

    if os.path.isfile(dest):
        with open(dest, "a") as o:
            o.write("\n\n# ADDED BY FETCHING LIBRARY \n\n")
            o.write(content)
    else:
        with open(dest, "w") as o:
            o.write(content)


parser = argparse.ArgumentParser()
parser.add_argument("--token", action="store")
parser.add_argument("--targets", action="store")
parser.add_argument("--dest", action="store")
args = parser.parse_args()

source, reqs = fetch(ast.literal_eval(args.targets), args.token)
out_file = args.dest if args.dest is not None else "dependencies.py"

write_output(out_file, source)
write_output("requirements.txt", reqs)

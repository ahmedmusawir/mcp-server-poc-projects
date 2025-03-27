# save as show_tree.py
import os

def print_tree(start_path, max_depth=2, prefix=""):
    for root, dirs, files in os.walk(start_path):
        depth = root[len(start_path):].count(os.sep)
        if depth > max_depth:
            continue
        indent = " " * 4 * depth
        print(f"{indent}{os.path.basename(root)}/")
        subindent = " " * 4 * (depth + 1)
        for f in files:
            print(f"{subindent}{f}")

if __name__ == "__main__":
    print_tree(".", max_depth=2) 

import hashlib
import sys

def parse_tree(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    tree = {}
    current_level = None
    left_node = None
    right_node = None
    for line in lines:
        line = line.strip()
        if line.startswith("Level"):
            current_level = int(line.split()[1].rstrip(':'))
            if current_level not in tree:
                tree[current_level] = []
        elif line.startswith("Left:"):
            left_node = line.split(":")[1].strip()
        elif line.startswith("Right:"):
            right_node = line.split(":")[1].strip()
            if current_level is not None and left_node is not None and right_node is not None:
                tree[current_level].extend([left_node, right_node])
            left_node = None
            right_node = None
        elif line.startswith("Root:"):
            current_level = current_level + 1
            max_level = current_level
            tree[current_level] = line.split(":")[1].strip()


    grouped_tree = {}
    for level, nodes in tree.items():
        if level != max_level:
            grouped_tree[level] = list(zip(nodes[::2], nodes[1::2]))
        else:
            grouped_tree[level] = nodes
    return grouped_tree

def find_path(tree, search_value):
    search_value = hashlib.sha256(search_value.encode('utf-8')).hexdigest()
    path = []
    current_level = 0

    for pair in tree[current_level]:
        if search_value in pair:
            index = pair.index(search_value)
            partner = pair[1 - index]
            path.append(partner)
            if index == 0:
                search_hash = hashlib.sha256((search_value + partner).encode('utf-8')).hexdigest()
            else:
                search_hash = hashlib.sha256((partner + search_value).encode('utf-8')).hexdigest()
            break
    else:
        return "no", []

    while current_level < max(tree.keys()):
        current_level += 1
        for pair in tree[current_level]:
            if search_hash in pair:
                index = pair.index(search_hash)
                partner = pair[1 - index]
                path.append(partner)
                if index == 0:
                    search_hash = hashlib.sha256((search_hash + partner).encode('utf-8')).hexdigest()
                else:
                    search_hash = hashlib.sha256((partner + search_hash).encode('utf-8')).hexdigest()
                break
        else:
            break

    return "yes", path

def main():
    search_value = sys.argv[1]
    filename = "merkle.tree"

    tree = parse_tree(filename)
    result, path = find_path(tree, search_value)

    if result == "yes":
        print("yes","[", ', '.join(path),"]")
    else:
        print("no")

if __name__ == "__main__":
    main()
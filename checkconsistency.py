import hashlib
import sys

class MerkleTreeNode:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value
        self.hashValue = hashlib.sha256(value.encode('utf-8')).hexdigest()

def buildTree(leaves, f, tree_name):
    f.write(f"{tree_name}:\n") 
    nodes = []
    f.write(f"Leaf Nodes:\n")
    for i, leaf in enumerate(leaves):
        f.write(f" Data Item {i+1}: {leaf.strip()}\n")
        hash_value = hashlib.sha256(leaf.strip().encode('utf-8')).hexdigest()
        f.write(f" Hash Value: {hash_value}\n")
        node = MerkleTreeNode(hash_value)
        nodes.append(node)

    level = 0
    while len(nodes) > 1:
        temp = []
        f.write(f"\nLevel {level}:\n")
        for i in range(0, len(nodes), 2):
            node1 = nodes[i]
            if i + 1 < len(nodes):
                node2 = nodes[i + 1]
            else:
                node2 = MerkleTreeNode(node1.value)
            concatenatedValue = node1.value + node2.value
            parent = MerkleTreeNode(concatenatedValue)
            parent.left = node1
            parent.right = node2
            f.write(f" Left: {node1.value}\n")
            f.write(f" Right: {node2.value}\n")
            f.write(f" PARENT(hash of concatenation): {parent.hashValue}\n")
            temp.append(parent.hashValue)
        if len(temp) == 1:
            root_value = temp[0]
            root = MerkleTreeNode(root_value)
            break 
        nodes = [MerkleTreeNode(value) for value in temp]
        level += 1

    f.write(f"\nRoot: {root.value}\n")
    return root

def check_order(input1, input2):
    for i, item in enumerate(input1):
        if item in input2:
            if input2.index(item) != i:
                return False
        else:
            return True
    return True


inputString = ','.join(sys.argv[1:])
input1, input2 = inputString.split('],[')
input1 = input1.replace('[', '')
input2 = input2.replace(']', '')

leaves1 = [leaf.strip() for leaf in input1.split(",")]
leaves2 = [leaf.strip() for leaf in input2.split(",")]


with open("merkle_trees.txt", "w") as f:
    root1 = buildTree(leaves1, f, "Merkle Tree 1")
    f.write("\n")
    root2 = buildTree(leaves2, f, "Merkle Tree 2")

result=check_order(leaves1, leaves2)
def parse_trees(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    trees = {}
    current_tree = None
    current_level = None
    left_node = None
    right_node = None
    max_levels = {}
    for line in lines:
        line = line.strip()
        if line.startswith("Merkle Tree"):
            current_tree = line.split(" - ")[0]
            trees[current_tree] = {}
            current_level = None
            max_levels[current_tree] = None
        elif line.startswith("Level"):
            current_level = int(line.split()[1].rstrip(':'))
            if current_level not in trees[current_tree]:
                trees[current_tree][current_level] = []
        elif line.startswith("Left:"):
            left_node = line.split(":")[1].strip()
        elif line.startswith("Right:"):
            right_node = line.split(":")[1].strip()
            if current_level is not None and left_node is not None and right_node is not None:
                trees[current_tree][current_level].extend([left_node, right_node])
            left_node = None
            right_node = None
        elif line.startswith("Root:"):
            current_level = current_level + 1
            max_levels[current_tree] = current_level
            trees[current_tree][current_level] = line.split(":")[1].strip()

    grouped_trees = {}
    for tree_name, tree in trees.items():
        grouped_tree = {}
        max_level = max_levels[tree_name]
        for level, nodes in tree.items():
            if level != max_level:
                grouped_tree[level] = list(zip(nodes[::2], nodes[1::2]))
            else:
                grouped_tree[level] = nodes
        grouped_trees[tree_name] = grouped_tree

    return grouped_trees

def find_root_in_other_tree(grouped_trees):
    tree_names = list(grouped_trees.keys())
    if len(tree_names) < 2:
        return "Not enough trees to compare."
    
    print()
    tree1_name = tree_names[0]
    tree2_name = tree_names[1]
    tree1 = grouped_trees[tree1_name]
    tree2 = grouped_trees[tree2_name]
    max_level_tree1 = max(tree1.keys())
    max_level_tree2 = max(tree2.keys())
    tree1_root = tree1[max_level_tree1] 
    tree2_root = tree2[max_level_tree2]  
    
    if tree1_root == tree2_root:
        return "Yes", tree1_root, ["Tree is the same"], tree2_root

    for level in range(max_level_tree2):
        nodes = tree2[level]
        for node_pair in nodes:
            if tree1_root in node_pair:
                partner_index = node_pair.index(tree1_root)
                partner = node_pair[1 - partner_index]
                min_path = find_min_path(grouped_trees, tree1_root, partner, level, max_level_tree2)
                return "Yes", tree1_root, min_path, tree2_root
    
    return "No", None, None, None

def find_min_path(grouped_trees, root_node, partner_node, level, max_level):
    tree_name = list(grouped_trees.keys())[1] 
    tree = grouped_trees[tree_name]
    path = [partner_node]
    current_hash = hashlib.sha256((root_node + partner_node).encode('utf-8')).hexdigest()

    while level < max_level:
        level += 1
        for pair in tree[level]:
            if current_hash in pair:
                index = pair.index(current_hash)
                partner = pair[1 - index]
                path.insert(0, current_hash) 
                if index == 0:
                    current_hash = hashlib.sha256((current_hash + partner).encode('utf-8')).hexdigest()
                else:
                    current_hash = hashlib.sha256((partner + current_hash).encode('utf-8')).hexdigest()
                break

    return path



final = parse_trees("merkle_trees.txt")
if result==True:
    string, root1, min_path, root2 = find_root_in_other_tree(final)
    if string == "Yes":
        print(string, "[",root1, ",",', '.join(min_path),",",root2, "]")
    else:
        print(string)
else:
    print("No")
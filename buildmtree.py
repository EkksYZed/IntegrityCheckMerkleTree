import hashlib
import sys
import re

class MerkleTreeNode:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value
        self.hashValue = hashlib.sha256(value.encode('utf-8')).hexdigest()

def buildTree(leaves, f):
    nodes = []
    f.write("Leaf Nodes:\n")
    for i, leaf in enumerate(leaves):
        f.write(f"    Data Item {i+1}: {leaf.strip()}\n")
        hash_value = hashlib.sha256(leaf.strip().encode('utf-8')).hexdigest()
        f.write(f"    Hash Value: {hash_value}\n")
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

            f.write(f"    Left: {node1.value}\n")
            f.write(f"    Right: {node2.value}\n")
            f.write(f"    PARENT(hash of concatenation): {parent.hashValue}\n")
            temp.append(parent.hashValue)

        if len(temp) == 1:
            root_value = temp[0]
            root = MerkleTreeNode(root_value)
            break

        nodes = [MerkleTreeNode(value) for value in temp]
        level += 1

    f.write(f"\nRoot: {root.value}\n")
    return root

inputString = ','.join(sys.argv[1:])


leavesString = inputString.replace('[', '').replace(']', '')
leaves = [leaf.strip() for leaf in leavesString.split(",")] 

with open("merkle.tree", "w") as f:
    root = buildTree(leaves, f)
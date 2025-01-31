from lark import Tree

def children_expander(tree):
    childrens = []
    for child in tree.children:
        if isinstance(child, Tree):
            childrens.extend(children_expander(child))
        else:
            childrens.append(child)
    return childrens

def children_to_string(tree):
    return ''.join(children_expander(tree))
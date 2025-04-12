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


def process_to_channel(processes: dict, separator: str = "2"):
    output_dict = {}
    for process, messages in processes.items():
        output_dict[process] = {}
        i = 0
        message = None
        while i < len(messages):
            message = messages[i]
            if not isinstance(message, dict):
                i += 1
                message = None
                continue
            break
        if message:
            channel_pair = message["channel"].split(separator)
            output_dict[process] = channel_pair[0] if message["statement"] == "out" else channel_pair[1]
        if not output_dict[process]:
            output_dict.pop(process)

    return output_dict

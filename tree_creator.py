from bigtree import Node

class Message(Node):
    def __init__(self, statement: str, channel: str, message: str):
        super().__init__(f"{statement} {channel} {message}")
        self.statement = statement
        self.channel = channel
        self.message = message


def create_tree(processes: dict, target_process: str, channel_mapping: dict, separator: str = "2", indexes=None):
    processes_to_check = processes[target_process]
    process_name_to_index = {channel_mapping[process]: i for i, process in enumerate(processes_to_check)}
    if indexes is None:
        indexes = [0 for _ in range(len(processes_to_check))]
    root = Node(processes_to_check[0])
    current_node = root
    current_process = 0
    deepsec_channel = None
    branches = []
    while True:
        if all(x == -1 for x in indexes):
            break
        process_name = processes_to_check[current_process]
        message = processes[process_name][indexes[current_process]]
        if isinstance(message, dict):
            node = Node(f"{message['statement']} {message['channel']} {message['message']}")
            current_node.append(node)
            current_node = node
            indexes[current_process] += 1
            if len(processes[process_name]) == indexes[current_process]:
                indexes[current_process] = -1
            channel_pair = message["channel"].split(separator)
            next_process = channel_pair[1]
            if deepsec_channel is None:
                deepsec_channel = channel_pair[0] if message["statement"] == "in" else channel_pair[1]
            elif next_process != deepsec_channel:
                current_process = process_name_to_index[next_process]
            elif next_process == deepsec_channel and indexes[current_process] == len(processes[process_name])-1:
                break
        else:
            node = Node(name="tmp")
            if message == "if":
                node.name = "if"
                current_node.append(node)
                branches.append((current_node, indexes.copy()))
                current_node = node
                # TODO the best way to handle branching is recursively calling the function and then skipping lines until the corresponding else is met
            elif message == "else":
                node.name = "else"
                current_node, old_indexes = branches.pop()
                for i, index in enumerate(old_indexes):
                    if i != current_process:
                        indexes[i] = index
                current_node = current_node.append(node)
                current_node = node
            elif message == "0":
                node.name = "0"
                current_node.append(node)
                current_node = node
            indexes[current_process] += 1
            if len(processes[process_name]) == indexes[current_process]:
                indexes[current_process] = -1

from copy import deepcopy
from lark import Visitor
from utils import children_to_string


class MessagesFinder(Visitor):
    """
    Class to find the messages exchanged between processes in a DPS file.
    """
    _processes = {}
    _current_process = None
    _actual_statement = None
    _current_channel = None
    _func_content_counter = 0

    def assignment(self, tree):
        if self._current_process is None:
            self._current_process = tree.children[0].children[0].value
            self._processes[self._current_process] = []

    def statement(self, tree):
        if tree.children[0].data != "func_content":
            self._actual_statement = tree.children[0].data

    def func_content(self, tree):
        if self._actual_statement in ["in", "out"]:
            if self._current_channel is None and len(tree.children) == 1:
                # todo: check if the channel is valid
                self._current_channel = tree.children[0].value
                message_dict = {
                    "statement": self._actual_statement,
                    "channel": self._current_channel,
                    "message": ""
                }
                self._processes[self._current_process].append(message_dict)
            elif self._current_channel:
                self._processes[self._current_process][-1]["message"] = children_to_string(
                    tree)
                self._current_channel = None

    def dot(self, _):
        self._current_process = None
        self._current_channel = None

    def if_statement(self, _):
        self._current_channel = None
        self._processes[self._current_process].append("if")

    def else_statement(self, _):
        self._current_channel = None
        self._processes[self._current_process].append("else")

    def semicolon(self, _):
        self._current_channel = None

    def constant(self, tree):
        if self._current_process:
            self._processes[self._current_process].append(
                tree.children[0].value)

    def output(self):
        return deepcopy(self._processes)

    def visit(self, tree):
        raise NotImplementedError("Use visit_topdown instead")


class QueryFinder(Visitor):
    _current_process = None
    _processes = {}

    def assignment(self, tree):
        if self._current_process is None:
            self._current_process = tree.children[0].children[0].value
            self._processes[self._current_process] = []
    
    def statement(self, tree):
        if self._current_process:
            if tree.children[0].data == "func_content":
                self._processes[self._current_process].append(children_to_string(tree))
            else:
                self._processes[self._current_process].append(tree.children[0].data)

    def query(self, tree):
        if self._current_process is None:
            self._current_process = "query"
            self._processes[self._current_process] = []

    def dot(self, _):
        self._current_process = None

    def output(self):
        processes = self._processes["query"][0].split(",")
        processes = [p.strip("(").strip(")") for p in processes]
        output_dict = {k:v for k,v in self._processes.items() if k in processes}
        for k,v in output_dict.items():
            output_dict[k] = [x for x in v if x not in ["dot", "pipe"]]
        output_dict["query"] = processes
        return output_dict

    def visit(self, tree):
        raise NotImplementedError("Use visit_topdown instead")
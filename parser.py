from lark import Lark
from visitor import MessagesFinder, QueryFinder
import pprint
import json

with open('deepsec.lark', 'r', encoding="utf-8") as grammar_file:
    grammar = grammar_file.read()

parser = Lark(grammar, parser='lalr')

with open('com-adaptive.dps', 'r', encoding="utf-8") as input_file:
    input_text = input_file.read()

tree = parser.parse(input_text)

message_finder = MessagesFinder()
message_finder.visit_topdown(tree)
output_dict = message_finder.output()
with open("result.json", "w", encoding="utf-8") as result_file:
    json.dump(output_dict, result_file, indent=4)
query_finder = QueryFinder()
query_finder.visit_topdown(tree)
query_dict = {}
for k, v in query_finder.output().items():
    query_dict[k] = v

with open("result.json", "w", encoding="utf-8") as result_file:
    json.dump(output_dict, result_file, indent=4)

with open("queries.json", "w", encoding="utf-8") as queries_file:
    json.dump(query_dict, queries_file, indent=4)

with open("processes.txt", "w", encoding="utf-8") as processes_file:
    for process in output_dict.keys():
        processes_file.write(f"{process}\n")



# print(tree.pretty())

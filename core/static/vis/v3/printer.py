import pprint

__author__ = 'spencertank'
import sys
import ast
pp = pprint.PrettyPrinter(indent=4)
data = sys.stdin.read()
data_dict = ast.literal_eval(data)
pp.pprint(data_dict)
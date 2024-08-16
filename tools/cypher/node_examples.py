examples = """
1. nodes of the Calculation view
MATCH (node:CVNode {{parentCV : "CalcView"}})
RETURN node

2. how many nodes are in the calculation view
MATCH (node:CVNode {{parentCV : "CalcView"}})
RETURN count(node)
"""

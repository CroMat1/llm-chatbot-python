
prefix = """
Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
If lineage is requested in question use the example 1 as reference.
Schema:
{schema}
Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

Fine Tuning:
For semantic, semantics use Semantics.
The node is parent_node and calc view, calculation view is parent_cv.
If parent_node is not specified in prompt use Semantics

Example Cypher Statements:

"""

suffix="""
The question is:
{question}"""
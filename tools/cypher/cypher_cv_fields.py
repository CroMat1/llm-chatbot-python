from llm import llm
from graph import graph

# Create the Cypher QA chain
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains import GraphCypherQAChain

CYPHER_GENERATION_TEMPLATE = """
Task:Generate Cypher statement to query a graph database.

Instructions:
Use only the provided relationship types and properties in the schema.
Schema:
{schema}

Do not use any other relationship types or properties that are not provided.

Note: 
Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

Fine Tuning:
for fields refer to label CVField

Example Cypher Statements:

1. Give the CVfields of a view CalcView
MATCH (cv:CalculationView {{name: "CalcView"}}) -[:HAS_FIELD]->(field:CVField) 
RETURN field

The question is:
{question}"""

prompt = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)
# I want the lineage of CHSBVERS of calc view ZSAC.ZBDG.ZRETAIL.ZHS/CVHSB001
cypher_fields = GraphCypherQAChain.from_llm(
    llm = llm,
    graph=graph,
    verbose=True,
    cypher_prompt=prompt,
    return_direct = True
)


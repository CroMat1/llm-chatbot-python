import streamlit as st
from llm import llm
from graph import graph

# Create the Cypher QA chain
from langchain_core.prompts.prompt import PromptTemplate
from langchain.chains import GraphCypherQAChain

# tag::cypher-qa[]
CYPHER_GENERATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
{schema}
Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

Examples: Here are a few examples of generated Cypher statements for particular questions:

1. CVField Lineage
match Path = (start:CVField ) -[:IS_MAPPED*]-(end:DBField) 
RETURN Path

The question is:
{question}"""

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)


cypher_qa = GraphCypherQAChain.from_llm(
    llm = llm,
    graph=graph,
    verbose=True,
    cypher_prompt=CYPHER_GENERATION_PROMPT
)
# end::cypher-qa[]

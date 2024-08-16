import streamlit as st
from llm import llm
from graph import graph
from tools.cypher.header import prefix, suffix
from tools.cypher.lineage_examples import examples

# Create the Cypher QA chain
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains import GraphCypherQAChain


# tag::cypher-qa[]
CYPHER_GENERATION_TEMPLATE = prefix + examples + suffix 

prompt = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)
# I want the lineage of CHSBVERS of calc view ZSAC.ZBDG.ZRETAIL.ZHS/CVHSB001
cypher_qa = GraphCypherQAChain.from_llm(
    llm = llm,
    graph=graph,
    verbose=True,
    cypher_prompt=prompt,
    return_direct = True
)
# end::cypher-qa[]

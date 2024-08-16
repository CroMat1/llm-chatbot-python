import streamlit as st
import header, Examples_Lineage

# Create the Cypher QA chain
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains import GraphCypherQAChain

example_prompt = PromptTemplate.from_template(
    "User input: {question}\nCypher query: {query}"
)
prompt = FewShotPromptTemplate(
    examples=Examples_Lineage.examples,
    example_prompt=example_prompt,
    prefix= header.prefix,
    suffix=header.suffix,
    input_variables=["question", "schema"],
)

print(prompt.format(question="Give me your soul?", schema="foo"))
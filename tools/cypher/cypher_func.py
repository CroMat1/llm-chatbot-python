import streamlit as st
from llm import llm
from graph import graph
from tools.cypher.prompt_fixed import prefix, suffix
from tools.cypher.lineage_examples import examples as lineage_examples
from tools.cypher.cvinfo_examples import examples as info_examples
from tools.cypher.node_examples import examples as node_examples

# Create the Cypher QA chain
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains import GraphCypherQAChain

# tag::lineage[]
def cypherLineage():

    CYPHER_GENERATION_TEMPLATE = prefix + lineage_examples + suffix 

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

    return cypher_qa
# end::lineage[]

# tag::CvInfo[]
def cypherCvInfo():

    CYPHER_GENERATION_TEMPLATE = prefix + info_examples + suffix 

    prompt = PromptTemplate(
        input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
    )
    
    cypher_qa = GraphCypherQAChain.from_llm(
        llm = llm,
        graph=graph,
        verbose=True,
        cypher_prompt=prompt,
        return_direct = True
    )

    return cypher_qa
    
# end::info[]

# tag::NodeInfo[]
def cypherNodeInfo():

    CYPHER_GENERATION_TEMPLATE = prefix + node_examples + suffix 

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

    return cypher_qa
# end::lineage[]
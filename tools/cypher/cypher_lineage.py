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
If lineage is requested in question use the example 1 as reference.

Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

Fine Tuning:
For semantic, semantics use Semantics.
The node is parent_node and calc view, calculation view is parent_cv.
If parent_node is not specified in prompt use Semantics

Example Cypher Statements:

1. Lineage of CV Field of CalcView and CVNode with all the element of the path
match Path = (start:CVField {{Name:"StartingCVField", parentCV : "Calc_View", parent_node :"CVNode"}} ) -[:IS_MAPPED*]-(end:DBField) 
UNWIND Nodes(Path) as element
RETURN 
  element.Name as Field, 
  CASE 
    WHEN "DBField" IN labels(element) THEN element.Object
    ELSE element.parent_node 
  END AS Object, 
  CASE 
    WHEN "DBField" IN labels(element) THEN element.Schema
    ELSE element.parentCV
  END AS Source

2. Lineage of CV Starting CV Field of CalcView with all the element of the path
match Path = (start:CVField {{Name:"StartingCVField", parentCV : "Calc_View", parent_node :"Semantics"}} ) -[:IS_MAPPED*]-(end:DBField) 
UNWIND Nodes(Path) as element
RETURN 
  element.Name as Field, 
  CASE 
    WHEN "DBField" IN labels(element) THEN element.Object
    ELSE element.parent_node 
  END AS Object, 
  CASE 
    WHEN "DBField" IN labels(element) THEN element.Schema
    ELSE element.parentCV
  END AS Source

The question is:
{question}"""

prompt = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)
# I want the lineage of CHSBVERS of calc view ZSAC.ZBDG.ZRETAIL.ZHS/CVHSB001
cypher_lineage = GraphCypherQAChain.from_llm(
    llm = llm,
    graph=graph,
    verbose=True,
    cypher_prompt=prompt,
    return_direct = True
)


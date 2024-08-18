import logging
from llm import llm
from graph import graph
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain.schema import StrOutputParser
from langchain.tools import Tool
from langchain_community.chat_message_histories import Neo4jChatMessageHistory
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from utils.utils import get_session_id

# Import tools
from tools.cypher.cypher_lineage import cypher_lineage
from tools.cypher.cypher_cv_info import cypher_cv
from tools.cypher.cypher_cv_fields import cypher_fields

# Configurazione logging
logging.basicConfig(level=logging.INFO)

# Funzione per creare il prompt della chat
def create_chat_prompt():
    return ChatPromptTemplate.from_messages(
        [
            ("system", "You are an Engie Graph expert providing information about CV Metadata."),
            ("human", "{input}"),
        ]
    )

# Funzione per configurare i tool
def configure_tools():
    general_chat = create_chat_prompt() | llm | StrOutputParser()
    
    return [
        Tool.from_function(
            name="General Chat",
            description="For general Info chat not covered by other tools",
            func=general_chat.invoke,
        ),
        Tool.from_function(
            name="Calculation View Information",
            description="Answer to all the questions related to the calculation view",
            func=cypher_cv
        ),
        Tool.from_function(
            name="CVFields Information",
            description="Answer to all the questions related to the fields of calculation view",
            func=cypher_fields
        ),
        Tool.from_function(
            name="Lineage",
            description="Provide information about Lineage",
            func=cypher_lineage
        )
    ]

# Funzione per gestire la memoria della sessione
def get_memory(session_id):
    try:
        return Neo4jChatMessageHistory(session_id=session_id, graph=graph)
    except Exception as e:
        logging.error(f"Error initializing message history: {e}")
        return None

# Funzione per creare il prompt dell'agent
def create_agent_prompt():
    return PromptTemplate.from_template("""
    You are my graph expert providing information about NEO4J Loaded Graph.
    Be as helpful as possible and return as much information as possible.
    Do not answer any questions that do not relate to Cypher, Graph, SQL, HANA, Calculation Views and NEO4J.

    Do not answer any questions using your pre-trained knowledge, only use the information provided in the context.

    TOOLS:
    ------
    You have access to the following tools:

    {tools}

    To use a tool, please use the following format:

    ```
    Thought: Do I need to use a tool? Yes
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ```

    When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

    ```
    Thought: Do I need to use a tool? No
    Final Answer: [your response here]
    ```

    Begin!

    Previous conversation history:
    {chat_history}

    New input: {input}
    {agent_scratchpad}
    """)

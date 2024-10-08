from llm import llm
from graph import graph
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.tools import Tool
from langchain_community.chat_message_histories import Neo4jChatMessageHistory
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain import hub
from utils.utils import get_session_id

# tag::import_cypher[]
from tools.cypher.cypher_lineage import cypher_lineage
from tools.cypher.cypher_cv_info import cypher_cv
from tools.cypher.cypher_cv_fields import cypher_fields
# end::import_cypher[]

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a Engie Graph expert providing information about CV Metadata."),
        ("human", "{input}"),
    ]
)

general_chat = chat_prompt | llm | StrOutputParser()

tools = [
    Tool.from_function(
        name="General Chat",
        description="For general Info chat not covered by other tools",
        func= general_chat.invoke,
    ), 
    Tool.from_function(
        name="Calculation View Information",
        description="Answer to all the questions related to the calculation view",
        func = cypher_cv
    ),    
    Tool.from_function(
        name="CVFields Information",
        description="Answer to all the questions related to the fields of calculation view",
        func = cypher_fields
    ),     
    Tool.from_function(
        name="Lineage",
        description="Provide information about Lineage ",
        func = cypher_lineage
    )    
]

def get_memory(session_id):
    return Neo4jChatMessageHistory(session_id=session_id, graph=graph)

agent_prompt = PromptTemplate.from_template("""
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

agent = create_react_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
    )

chat_agent = RunnableWithMessageHistory(
    agent_executor,
    get_memory,
    input_messages_key="input",
    history_messages_key="chat_history"
)

def generate_response(user_input):
    """
    Create a handler that calls the Conversational agent  and returns a response to be rendered in the UI
    """
    response = chat_agent.invoke(
            {"input": user_input},
            {"configurable": 
                {
                    "session_id": get_session_id()
                }
            }
        )

    return response['output']

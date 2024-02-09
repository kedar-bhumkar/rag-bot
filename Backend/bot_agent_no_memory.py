from langchain_openai import ChatOpenAI
from langchain.agents import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
from function_def import *
from prompt import *


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

tools = [checkUserExitsIinACL, addUserInACL]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            CUSTOMER_SUPPORT_AGENT,
        ),
        ("user", "Question from the user : {input}. \ Context :" + context1),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

llm_with_tools = llm.bind_tools(tools)

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


list(agent_executor.stream({"input": "{user_question}"}))


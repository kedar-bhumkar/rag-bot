from langchain_openai import ChatOpenAI
from langchain.agents import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor

from function_def import *
from prompt import *
from indexer import *
MEMORY_KEY = "chat_history"

cache ={}
def chat( userId, user_input):
    chat_history = []
    
    if userId not in cache:
        cache[userId]= []
    else:
        chat_history =  cache.get(userId)
    
    print('cache -' , cache)
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    tools = [checkUserExitsIinACL, addUserInACL]

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                CUSTOMER_SUPPORT_AGENT,
            ),
            MessagesPlaceholder(variable_name=MEMORY_KEY),        
            ("user", "Question from the user : {input}."),
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
        "chat_history": lambda x: x["chat_history"],

        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    context = getContext( user_input)
    #print("Bot context - " + context)
    #print("chat history" , chat_history)
    result = agent_executor.invoke({"input": "User Question-" + user_input + "Provided Context -" + context, "chat_history": chat_history})
    chat_history.extend(
        [
            HumanMessage(content=user_input),
            AIMessage(content=result["output"]),
        ]
    )    
    cache[userId]= chat_history

    return result
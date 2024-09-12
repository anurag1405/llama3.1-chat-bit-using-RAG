from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from models.query import Query
from utils.vector_store import tools
from langchain_community.llms import Ollama
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun

# Initialize LangChain components
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
Arxivwrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)
tools.extend([WikipediaQueryRun(api_wrapper=api_wrapper), ArxivQueryRun(api_wrapper=Arxivwrapper)])

template = '''Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat strictly up to 10 times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

If you are confident that you know the answer before reaching the limit, stop early and provide the Final Answer.

Begin!

Question: {input}
Thought:{agent_scratchpad}'''
prompt = PromptTemplate.from_template(template)

async def handle_agent_query(query: Query):
    llm = Ollama(model='llama3.1', temperature=0)
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=10)

    try:
        result = agent_executor.invoke({"input": query.query})
        return {"result": result['output']}
    except Exception as e:
        return {"error": str(e)}

import os
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI

# Import the tools from tools.py
from tools import detect_filler_words, detect_repetitive_phrases, detect_long_sentences, detect_long_pauses, check_star_structure, score_relevance

# Load environment variables
load_dotenv()

# 1. Define State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Setup Agent and Tools
tools = [detect_filler_words, 
         detect_repetitive_phrases, 
         detect_long_sentences, 
         detect_long_pauses, 
         check_star_structure, 
         score_relevance]

base_url = "https://openrouter.ai/api/v1"
api_key = os.getenv("Open_API_KEY")

llm = ChatOpenAI(
    model="nvidia/nemotron-3.5-lightning:free", 
    base_url= base_url,
    api_key=api_key)

llm_with_tools = llm.bind_tools(tools)

def evaluator_node(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# 3. Build the Single-Turn Graph (No memory yet)
graph_builder = StateGraph(State)
graph_builder.add_node("evaluator", evaluator_node)
graph_builder.add_node("tools", ToolNode(tools))

graph_builder.add_edge(START, "evaluator")
graph_builder.add_conditional_edges("evaluator", tools_condition)
graph_builder.add_edge("tools", "evaluator")

interview_agent = graph_builder.compile()

# 4. End-to-End Evaluation Test
if __name__ == "__main__":
    question = "Tell me about a time you handled a difficult project."
    answer = "Um, basically the situation was tough. I was assigned a task to migrate data. I led the action, and the result was successful."
    expected_keywords = ["migrate", "data", "successful"]
    
    prompt = f"""You are an encouraging mock-interview coach. 
    The candidate was asked: '{question}'. 
    They answered: '{answer}'. 
    Expected keywords were: {expected_keywords}.
    Evaluate the answer using your tools, then produce short, encouraging feedback."""
    
    print("Evaluating answer...\n")
    events = interview_agent.stream(
        {"messages": [("user", prompt)]}, 
        stream_mode="values"
    )
    
    # Print of the final generated feedback
    final_message = list(events)[-1]["messages"][-1].content
    print("Feedback:")
    print(final_message)
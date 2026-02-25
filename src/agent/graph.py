import json
from typing import TypedDict, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage, HumanMessage

from src.tools.scraper import scrape_job_url
from src.agent.prompts import EXTRACT_REQUIREMENTS_PROMPT, REWRITE_CV_PROMPT, EVALUATE_CV_PROMPT

class AgentState(TypedDict):
    url: str
    raw_cv: str
    job_description: Optional[str]
    job_requirements: Optional[str]
    rewritten_cv: Optional[str]
    initial_evaluation: Optional[dict]
    final_evaluation: Optional[dict]

def scrape_node(state: AgentState):
    """Scrapes the job description from the given URL."""
    print(f"Scraping job URL: {state['url']}")
    job_description = scrape_job_url.invoke({"url": state["url"]})
    return {"job_description": job_description}

def extract_node(state: AgentState):
    """Extracts the core requirements from the job description."""
    print("Extracting job requirements...")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = PromptTemplate.from_template(EXTRACT_REQUIREMENTS_PROMPT)
    chain = prompt | llm
    
    response = chain.invoke({"job_description": state["job_description"]})
    return {"job_requirements": response.content}

def rewrite_node(state: AgentState):
    """Rewrites the CV to align with the extracted job requirements."""
    print("\nRewriting CV (streaming)...")
    # Use streaming for the rewrite node
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, streaming=True)
    prompt = PromptTemplate.from_template(REWRITE_CV_PROMPT)
    chain = prompt | llm
    
    # We will invoke and let Langchain stream to stdout if we attach a callback, 
    # but since we want simple streaming for now we can just stream() and print
    # LangGraph nodes need to return the updated state.
    
    response_stream = chain.stream({
        "job_requirements": state["job_requirements"],
        "current_cv": state["raw_cv"]
    })
    
    rewritten_cv = ""
    for chunk in response_stream:
        print(chunk.content, end="", flush=True)
        rewritten_cv += chunk.content
        
    print("\n--- Rewrite Complete ---")
    return {"rewritten_cv": rewritten_cv}

def evaluate_initial_node(state: AgentState):
    """Evaluates the initial CV against the job requirements."""
    print("Evaluating initial CV...")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = PromptTemplate.from_template(EVALUATE_CV_PROMPT)
    chain = prompt | llm
    
    response = chain.invoke({
        "job_requirements": state["job_requirements"],
        "cv": state["raw_cv"]
    })
    
    try:
        evaluation = json.loads(response.content.strip("`").removeprefix("json\n"))
    except Exception as e:
        print(f"Error parsing evaluation JSON: {e}")
        evaluation = {"score": 0, "reasoning": "Failed to parse evaluation response.", "missing_skills": []}
        
    return {"initial_evaluation": evaluation}

def evaluate_final_node(state: AgentState):
    """Evaluates the rewritten CV against the job requirements."""
    print("Evaluating rewritten CV...")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = PromptTemplate.from_template(EVALUATE_CV_PROMPT)
    chain = prompt | llm
    
    response = chain.invoke({
        "job_requirements": state["job_requirements"],
        "cv": state["rewritten_cv"]
    })
    
    try:
        evaluation = json.loads(response.content.strip("`").removeprefix("json\n"))
    except Exception as e:
        print(f"Error parsing evaluation JSON: {e}")
        evaluation = {"score": 0, "reasoning": "Failed to parse evaluation response.", "missing_skills": []}
        
    return {"final_evaluation": evaluation}

def build_graph():
    """Builds and compiles the LangGraph."""
    workflow = StateGraph(AgentState)
    
    workflow.add_node("scrape", scrape_node)
    workflow.add_node("extract", extract_node)
    workflow.add_node("evaluate_initial", evaluate_initial_node)
    workflow.add_node("rewrite", rewrite_node)
    workflow.add_node("evaluate_final", evaluate_final_node)
    
    workflow.add_edge(START, "scrape")
    workflow.add_edge("scrape", "extract")
    workflow.add_edge("extract", "evaluate_initial")
    workflow.add_edge("evaluate_initial", "rewrite")
    workflow.add_edge("rewrite", "evaluate_final")
    workflow.add_edge("evaluate_final", END)
    
    return workflow.compile()

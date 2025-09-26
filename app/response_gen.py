import json
import os
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END
from langchain.schema import AIMessage, HumanMessage
from app.rag_layer import retrieve_context
from app.validation import validate_response
from app import config
import streamlit as st
from langsmith import Client

langsmith_client = Client() if config.LANGSMITH_API_KEY else None

with open("data/kb/few_shot_prompts.json", "r") as f:
    few_shot_data = json.load(f)

few_shot_examples = [
    {"user": ex["user"], "context": ex["context"], "response": ex["response"]}
    for ex in few_shot_data["examples"]
]

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{user}\nContext: {context}"),
    ("ai", "{response}")
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=few_shot_examples,
)

system_prompt = """
You are an empathetic mental health chatbot specializing in Omani Arabic. Respond in Omani dialect Arabic.
Use retrieved context and best practices: {best_practices}.
Be supportive, suggest resources, but never diagnose or give medical advice.
If crisis_risk is 'High Risk', respond with: "ياخي، أشوفك محتاج دعم فوري. تواصل مع مستشفى المسارة على 2487 3268 أو اتصل 9999 للطوارئ."
If crisis_risk is 'Medium Risk', include a CBT de-escalation technique from context and suggest professional help.
User query: {query}
Retrieved context: {context}
Emotions: {emotions}
Intent: {intent}
Crisis Risk: {crisis_risk}
"""

final_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    few_shot_prompt,
    ("human", "{query}")
])

# LLMs
gpt4 = ChatOpenAI(model="gpt-4o", api_key=config.OPENAI_API_KEY)
claude = ChatAnthropic(model="claude-3-opus-20240229", api_key=config.ANTHROPIC_API_KEY)

def generate_with_failover(query, context, emotions, intent, crisis_risk):
    chain = final_prompt | gpt4 | StrOutputParser()
    try:
        response = chain.invoke({
            "query": query,
            "context": context,
            "emotions": emotions,
            "intent": intent,
            "crisis_risk": crisis_risk,
            "best_practices": json.dumps(few_shot_data["best_practices"])
        })
        # Log to LangSmith
        if langsmith_client:
            langsmith_client.create_run(
                name="response_generation",
                inputs={"query": query, "crisis_risk": crisis_risk},
                outputs={"response": response},
                run_type="chain"
            )
        return response
    except Exception:
        # Failover to Claude
        chain = final_prompt | claude | StrOutputParser()
        response = chain.invoke({
            "query": query,
            "context": context,
            "emotions": emotions,
            "intent": intent,
            "crisis_risk": crisis_risk,
            "best_practices": json.dumps(few_shot_data["best_practices"])
        })
        if langsmith_client:
            langsmith_client.create_run(
                name="response_generation_failover",
                inputs={"query": query, "crisis_risk": crisis_risk},
                outputs={"response": response},
                run_type="chain"
            )
        return response

# LangGraph workflow: retrieve -> generate -> validate
class AgentState(TypedDict):
    query: str
    emotions: str
    intent: str
    crisis_risk: str
    context: str
    response: str
    validation_score: float

def retrieve(state: AgentState) -> AgentState:
    context_docs = retrieve_context(state["query"])
    state["context"] = "\n".join([doc.page_content for doc in context_docs])
    return state

def generate(state: AgentState) -> AgentState:
    state["response"] = generate_with_failover(
        state["query"], state["context"], state["emotions"], state["intent"], state["crisis_risk"]
    )
    return state

def validate(state: AgentState) -> AgentState:
    score, feedback = validate_response(state["response"], state["query"])
    state["validation_score"] = score
    if score < 0.7:  # Threshold for re-generation
        state["response"] = "Response invalidated. Regenerating..."  # Or re-run generate
    return state

workflow = StateGraph(AgentState)
workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)
workflow.add_node("validate", validate)
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", "validate")
workflow.add_edge("validate", END)
workflow.set_entry_point("retrieve")

app = workflow.compile()

def generate_response(query, emotions, intent, crisis_risk):
    inputs = {
        "query": query,
        "emotions": emotions,
        "intent": intent,
        "crisis_risk": crisis_risk
    }
    result = app.invoke(inputs)
    return result["response"]